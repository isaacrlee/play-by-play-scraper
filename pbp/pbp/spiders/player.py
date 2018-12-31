import scrapy
import re


class PlayerSpider(scrapy.Spider):
    name = "player"

    start_urls = ['http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20366',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20770',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20368',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20369',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20370',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20021',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20371',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20071',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20373',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20103',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20287',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20828',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20374',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20886',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20291',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20280',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20242',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20376',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20361',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21866',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20518',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20705',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20740',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21135',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20100',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20106',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20880',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21093',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20108',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20270',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20522',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21388',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20089',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20319',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21014',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20800',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20486',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21931',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21094',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20295',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20115',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20117',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20038',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20529',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20383',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20118',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20384',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20385',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20174',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20175',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20447',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20537',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20835',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20982',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20079',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20543',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21988',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20041',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20022',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20122',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20033',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20292',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21025',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20123',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20070',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20489',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20090',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21026',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20124',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20239',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20083',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20125',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20257',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21090',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20393',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20952',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20129',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20256',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20452',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=22025',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20565',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20396',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20131',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20566',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20132',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20398',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20134',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20135',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21089',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21098',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20040',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20401',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20403',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20846',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20010',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20779',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20276',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20004',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20140',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20065',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20790',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20577',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20240',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20142',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20246',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20251',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20145',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20204',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20147',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20408',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20219',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=22104',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20588',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21052',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20248',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20410',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=22122',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20491',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20069',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21054',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20216',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20411',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20412',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=22353',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20235',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20413',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20328',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20463',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20860',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20317',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20037',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21632',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20152',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20499',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20093',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20153',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20024',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20272',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20241',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20348',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20074',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20771',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21656',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20326',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20417',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20288',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20606',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20032',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20739',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20097',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20419',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20610',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20218',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20500',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21092',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20258',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20053',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20001',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20161',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20296',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20421',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21265',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20165',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20615',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20425',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20245',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20294',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20005',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20190',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20428',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20734',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20036',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20217',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20039',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20429',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20307',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20631',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20249',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20023',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=22240',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20433',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20434',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20016',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20169',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20334',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20435',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20336',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20173',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20054',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20367',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20881',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20048',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20439',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20026',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20344',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20492',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20440',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20008',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20442',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20029',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20232',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20304',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20494',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20443',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20357',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20223',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20896',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20078',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20176',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20177',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20350',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20045',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20450',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20254',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20178',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20891',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20179',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20454',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20017',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20648',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20456',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20457',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20180',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20213',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20297',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21095',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20181',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20346',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20018',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20182',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20183',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20011',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20085',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20458',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20066',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20460',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20255',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20266',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20498',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20006',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20652',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20861',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20502',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20215',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20342',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20462',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20151',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20214',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20465',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20185',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20358',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20186',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20466',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20092',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20187',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20325',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20009',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20091',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21767',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20353',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20049',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20015',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=22297',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20193',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20659',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21083',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20904',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20262',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20472',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20194',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20318',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20911',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20196',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21097',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20064',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20809',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20966',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20503',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20231',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20198',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20072',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20665',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20293',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21096',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20094',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20057',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20195',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20485',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20474',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20670',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20277',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20031',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20701',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=21091',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20030',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20506',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20314',
 'http://www.thebaseballcube.com/teams/roster.asp?Y=2018&T=20488']

    def parse(self, response):
        players = response.css('.dataRow')

        pattern = re.compile(r'(?<=T=)\w+')
        search = re.search(pattern, response.request.url)
        if bool(search):
            tbc_team_id = int(search.group(0))
        else:
            raise Exception('Bad Request')

        for player in players:
            cols = player.css('td')
            yield {
                'tbc_player_id': int(cols[1].css('a::attr(href)')[
                    0].re_first(r'(?<=ID=)\w+')),
                'first_name': cols[1].css('a::text')[0].re_first(r'^[\w\'\.-]+'),
                'last_name': cols[1].css('a::text')[
                    0].re_first(r'(?<= )[\w\'\.-]+'),
                'handedness': cols[5].css('::text').extract_first(),
                'tbc_team_id': tbc_team_id
            }