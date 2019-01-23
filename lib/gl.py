#_*_coding:utf-8_*_
import os,time
import reportLog
global libPath
global reportPath #报告路径
global casePath
global imgPath
global configPath
global dataPath
global curDate

logInstance = reportLog.cREPORTXML()


PATH =lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__),p))

'''全局变量'''
libPath = PATH(os.path.dirname(__file__)) #lib目录
reportPath = os.path.join(PATH(os.path.dirname(libPath)),'report')
casePath = os.path.join(PATH(os.path.dirname(libPath)),'testCase')
imgPath = os.path.join(PATH(reportPath),'images')
configPath = os.path.join(PATH(os.path.dirname(libPath)),'config')
dataPath = os.path.join(PATH(os.path.dirname(libPath)),'data')
curDate = time.strftime('%Y-%m-%d')
configFile = os.path.join(configPath,'config.yaml')



if __name__=="__main__":
    print "lib路径:%s"%libPath
    print "report路径:%s"%reportPath
    print 'testCase路径:{0}'.format(casePath)
    print 'report/images路径:{0}'.format(imgPath)
    print 'config路径:{0}'.format(configPath)
    print 'data路径:{0}'.format(dataPath)