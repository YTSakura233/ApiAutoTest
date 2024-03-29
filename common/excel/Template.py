from common.init.Init import Init
from common.utils.ExcelUtil import ExcelUtil

'''
@模板校验:校验各关键字是否存在，顺序是否正确，是否有重复关键字;校验各部分数量是否一致
@author: zohar
'''


def getCount(start, end):
    """
    获取各标志位之间的数组个数
    @param start: 开始列
    @param end: 结束列
    """
    return [column for column in range(start, end)]


class Template(Init):

    def verTemp(self, sheetName, sheet, bookRes, sheetRes, fileRes):
        """
        模板校验
        @param bookRes: 用例结果文件
        @param sheetName: 页签名
        @param sheet: 用例文件
        @param sheetRes: 用例结果文件
        @param fileRes: 用例结果文件
        """
        msg = self.verKeyWord(fileRes, sheet)
        blue = ExcelUtil.setCell(7)
        if '未找到关键字' in f'{msg}':
            self.setFonts('green', f'{sheetName}:', 'size=4')
            self.setFonts('red', msg)
            return msg
        elif '存在重复的关键字' in f'{msg}':
            self.setFonts('green', f'{sheetName}:', 'size=4')
            self.setFonts('red', msg)
            return msg
        elif '关键字顺序不正确' in f'{msg}':
            info = "['关键字顺序不正确'," + "'" + f'{ExcelUtil.getValue(fileRes, sheet, 1, msg[1])}' + "','" + \
                   f'{ExcelUtil.getValue(fileRes, sheet, 1, msg[2])}' + "']"
            if fileRes.endswith('xls'):
                sheetRes.write(1, msg[1], ExcelUtil.getValue(fileRes, sheet, 1, msg[1]), blue)
                sheetRes.write(1, msg[2], ExcelUtil.getValue(fileRes, sheet, 1, msg[2]), blue)
            elif fileRes.endswith('xlsx'):
                ExcelUtil.setColor(sheetRes, 2, msg[1], ExcelUtil.getValue(fileRes, sheet, 1, msg[1]), "blue")
                ExcelUtil.setColor(sheetRes, 2, msg[2], ExcelUtil.getValue(fileRes, sheet, 1, msg[2]), "blue")
            bookRes.save(fileRes)
            self.setFonts('green', f'{sheetName}:', 'size=4')
            self.setFonts('red', info)
            return msg
        else:
            info = self.verLength()
            if '数量不一致' in f'{info}':
                for i in range(1, len(info)):
                    if fileRes.endswith('.xls'):
                        sheetRes.write(1, int(info[i]), ExcelUtil.getValue(fileRes, sheet, 1, int(info[i])), blue)
                    elif fileRes.endswith('.xlsx'):
                        ExcelUtil.setColor(sheetRes, 2, int(info[i]), ExcelUtil.getValue(fileRes, sheet, 1, int(info[i])),
                                           "blue")
                bookRes.save(fileRes)
                self.setFonts('green', f'{sheetName}:', 'size=4')
                self.setFonts('red', info)
                return info
            else:
                return ''

    def verKeyWord(self, file, sheet):
        """
        校验各关键字是否存在，顺序是否正确，是否有重复关键字
        @param file: 用例文件
        @param sheet: 用例文件
        """
        listCopy = []
        order = []
        keyWord = ''
        msg = ["未找到关键字"]
        repeat = ['存在重复的关键字']
        # 定义关键字数组
        keyList = ['name', 'url', 'method', 'param', 'file', 'header', 'part101', 'part201', 'part301', 'section101',
                   'section201', 'section301', 'resText', 'resHeader', 'statusCode', 'expression', 'status', 'time',
                   'init001', 'restore001', 'dyparam001', 'key001', 'value001', 'headerManager', '数据库', 'Iteration']
        for item in keyList:
            for i in range(self.ncols):
                try:
                    if file.endswith('xls'):
                        keyWord = sheet.cell(1, i).value
                    elif file.endswith('xlsx'):
                        keyWord = sheet.cell(row=2, column=i).value
                except Exception as e:
                    print(e)
                if item == keyWord:
                    order.append(self.findStr(file, sheet, item))
                    if len(listCopy) > 0:
                        for k in range(len(listCopy)):
                            if item == listCopy[k]:
                                repeat.append(item)
                                break
                    listCopy.append(item)
            # 如果没找到关键字，则返回未找到的关键字
            if item not in listCopy:
                msg.append(item)
        if len(repeat) > 1:
            return repeat
        if len(msg) > 1:
            return msg
        # 找到全部关键字则校验顺序
        msg = ["关键字顺序不正确"]
        for i in range(len(order)):
            try:
                if i + 1 < len(order) and order[i + 1] < order[i]:
                    msg.append(order[i])
                    msg.append(order[i + 1])
            except Exception as e:
                print(e)
        return msg if len(msg) > 1 else ''

    def verLength(self):
        """
        校验各部分数量是否一致
        """
        msg = ["数量不一致"]
        # 校验字段
        len1 = getCount(self.part101Col, self.part201Col)
        len2 = getCount(self.part201Col, self.part301Col)
        len3 = getCount(self.part301Col, self.section101Col)
        # 预期结果
        len4 = getCount(self.section101Col, self.section201Col)
        len5 = getCount(self.section201Col, self.section301Col)
        len6 = getCount(self.section301Col, self.resTextCol)
        # 接口变量
        len7 = getCount(self.key001Col, self.value001Col)
        len8 = getCount(self.value001Col, self.headerManagerCol)
        if len(len1) != len(len4):
            return msg + len1 + len4
        elif len(len2) != len(len5):
            return msg + len2 + len5
        elif len(len3) != len(len6):
            return msg + len3 + len6
        elif len(len7) != len(len8):
            return msg + len7 + len8
        else:
            return ''
