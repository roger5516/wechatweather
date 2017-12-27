#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# useage: python3 main.py 2016-04-28
import datetime, sys, os, logging

log_file = "/data/roger/tmp/search/search.keywords.log"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s :%(funcName)s %(message)s',
                    datefmt='%a, %Y-%m-%d %H:%M:%S',
                    filename=log_file,
                    filemode='a')

# get yestoday's date
def get_date():
    delta = datetime.timedelta(days=1)
    today = datetime.datetime.now()
    yestoday = today - delta
    date = yestoday.strftime('%Y-%m-%d')
    if 2 == len(sys.argv):
        date = sys.argv[1]

    logging.info('处理日期为 ' + date)
    return date

# get flow data  which logtype in '10000' '20000' '30000' from hive
def get_pvdata_from_hive(date,trackerfile):
    logging.info("从hive中查数据!")
    os.system('''hive -e"
select servertime, fronttime, ip, guid,  nvl(userid,0) as userid, platformid, appid, platform, biztype, logtype, referurl, curpageurl, pagelevelid, viewid, viewparam, clickid, clickparam, os, display, downchann, appversion, devicetype, nettype, coordinate, hserecomkey, hseextend, hseepread, searchengine, keyword, chansource, search, hours, ten_min, levelid, country, province, city, district from (
	select c.servertime, c.fronttime, c.ip, c.guid,  case when c.userid is null then 0 else c.userid end as userid, c.platform, c.biztype, c.logtype, c.referurl, c.curpageurl, c.pagelevelid, c.viewid, c.viewparam, c.clickid, c.clickparam, c.os, c.display, c.downchann, c.appversion, c.devicetype, c.nettype, c.coordinate, c.hserecomkey, c.hseextend, c.hseepread, c.searchengine, c.keyword, c.chansource, c.search, c.hours, c.ten_min, nvl(d.levelid,5)  as levelid, c.country, c.province, c.city, c.district , c.platformid, c.appid
	from (
		select
		servertime, fronttime, ip, guid, userid, platform, biztype, logtype, referurl, curpageurl, pagelevelid, viewid, viewparam, clickid, clickparam, os, display, downchann, appversion, devicetype, nettype, coordinate, hserecomkey, hseextend, hseepread, searchengine, keyword, chansource, search, hours, ten_min , country, province, city, district, platformid, appid
		from fdm.fdm_tracker_detail_da
		where days='%s'
		and platform not in ('02','03')
		and  logtype ='20000'
		and clickid <>'20004'
		and concat( platformid ,'-',appid  ) <>'1-2'
		and concat( platformid ,'-',biztype  ) <>'1-006'
		and guid <>''
		and fronttime <>''
		and length(userid)>9
		and userid like '1%%'
		union
		select a.servertime, a.fronttime, a.ip, a.guid, b.userid, a.platform, a.biztype, a.logtype, a.referurl, a.curpageurl, a.pagelevelid, a.viewid, a.viewparam, a.clickid, a.clickparam, a.os, a.display, a.downchann, a.appversion, a.devicetype, a.nettype, a.coordinate, a.hserecomKey, a.hseextend, a.hseepread, a.searchengine, a.keyword, a.chansource, a.search, a.hours, a.ten_min, a.country, a.province, a.city, a.district , a.platformid, a.appid
		from (
			select 	servertime, fronttime, ip, guid, platform, biztype, logtype, referurl, curpageurl, pagelevelid, viewid, viewparam, clickid, clickparam, os, display, downchann, appversion, devicetype, nettype, coordinate, hserecomkey,hseextend, hseepread, searchengine, keyword, chansource, search, hours,ten_min , country, province, city, district , platformid, appid
			from fdm.fdm_tracker_detail_da
			where days='%s'
			and platform not in ('02','03')
			and  logtype ='20000'
			and clickid <>'20004'
		    and concat( platformid ,'-',appid  ) <>'1-2'
		    and concat( platformid ,'-',biztype  ) <>'1-006'
			and guid <>''
			and fronttime <>''
			and (userid like '%%==%%' or length(userid) <=9
			)
		) a
		left join
		(
			select guid,max(userid) as userid
			from fdm.fdm_guid_page_pv_ten_min_de
			where days='%s'
			and platform not in ('02','03')
            and concat( platformid ,'-',appid  ) <>'1-2'
	     	and concat( platformid ,'-',biztype  ) <>'1-006'
			and length(userid)>9
			and userid like '1%%'
			group by guid
		) b
		on a.guid = b.guid
	)c
	left join
	(
		select ad.platformid,ad.pagelevelid ,ad.biztype ,bd.logtype ,ad.viewid ,bd.clickid, bd.levelid from (
			select platformid,pagelevelid ,biztype  ,eventid as viewid
			from bdm.bdm_tracker_protocol where logtype='10000'
		) ad
		join
		(
			select platformid,pagelevelid ,biztype ,logtype ,eventid as clickid,levelid
			from bdm.bdm_tracker_protocol
			where logtype='20000'
		) bd
		on ad.platformid =bd.platformid and  ad.biztype=bd.biztype and ad.pagelevelid=bd.pagelevelid
	)d on d.platformid =c.platformid and  d.pagelevelid = c.pagelevelid and d.biztype =c.biztype and d.logtype=c.logtype and d.clickid = c.clickid
	union all
	select c.servertime, c.fronttime, c.ip, c.guid,  nvl(c.userid, 0) as userid, c.platform, c.biztype, c.logtype, c.referurl, c.curpageurl, c.pagelevelid, c.viewid, c.viewparam, c.clickid, c.clickparam, c.os, c.display, c.downchann, c.appversion, c.devicetype, c.nettype, c.coordinate, c.hserecomkey, c.hseextend, c.hseepread, c.searchengine, c.keyword, c.chansource, c.search, c.hours, c.ten_min, nvl(d.levelid,5)  as levelid, c.country, c.province, c.city, c.district, c.platformid, c.appid
	from (
		select servertime, fronttime, ip, guid, userid, platform, biztype, logtype, referurl, curpageurl, pagelevelid, viewid, viewparam, clickid, clickparam, os, display, downchann, appversion, devicetype, nettype, coordinate, hserecomkey, hseextend, hseepread, searchengine, keyword, chansource, search, hours, ten_min , country, province, city, district , platformid, appid
		from fdm.fdm_tracker_detail_da
		where days='%s'
		and platform not in ('02','03')
		and  logtype ='10000'
		and concat( platformid ,'-',appid  ) <>'1-2'
		and concat( platformid ,'-',biztype  ) <>'1-006'
		and guid <>''
		and fronttime <>''
		and length(userid)>9
		and userid like '1%%'
		union
		select a.servertime, a.fronttime, a.ip, a.guid, b.userid, a.platform, a.biztype, a.logtype, a.referurl, a.curpageurl, a.pagelevelid, a.viewid, a.viewparam, a.clickid, a.clickparam, a.os, a.display, a.downchann, a.appversion, a.devicetype, a.nettype, a.coordinate, a.hserecomKey, a.hseextend, a.hseepread, a.searchengine, a.keyword, a.chansource, a.search, a.hours, a.ten_min, a.country, a.province, a.city, a.district, a.platformid, a.appid
		from (
			select servertime, fronttime, ip, guid, platform, biztype, logtype, referurl, curpageurl, pagelevelid, viewid, viewparam, clickid, clickparam, os, display, downchann, appversion, devicetype, nettype, coordinate, hserecomkey, hseextend, hseepread, searchengine, keyword, chansource,search,hours, ten_min , country, province, city, district , platformid, appid
			from fdm.fdm_tracker_detail_da
			where days='%s'
			and platform not in ('02','03')
			and  logtype ='10000'
			and concat( platformid ,'-',appid  ) <>'1-2'
		    and concat( platformid ,'-',biztype  ) <>'1-006'
			and guid <>''
			and fronttime <>''
			and (userid like '%%==%%' or length(userid) <=9 )
		) a
		left join
		(
			select guid,max(userid) as userid
			from fdm.fdm_guid_page_pv_ten_min_de
			where days='%s'
			and platform not in ('02','03')
			and concat( platformid ,'-',appid  ) <>'1-2'
			and concat( platformid ,'-',biztype  ) <>'1-006'
			and length(userid)>9
			and userid like '1%%'
			group by guid
		) b
		on a.guid = b.guid
	)c
	left join (
		select platformid,pagelevelid ,biztype ,logtype, eventid ,levelid
		from bdm.bdm_tracker_protocol
		where logtype='10000'
	)d on d.platformid =c.platformid and d.pagelevelid = c.pagelevelid and d.biztype =c.biztype and d.logtype=c.logtype
	-- and d.eventid = c.viewid
)aaaa order by platformid,appid,guid,userid,fronttime
">%s''' % (date, date, date, date, date, date,trackerfile))
    count = len(open(trackerfile, 'rU').readlines())
    logging.info('hive found  %d  条数据' % (count))

# main
def main():
    date = get_date()
    get_pvdata_from_hive(date)


main()
