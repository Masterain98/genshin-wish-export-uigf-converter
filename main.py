from datetime import datetime, timezone, timedelta
import pandas as pd


def converter(fileName, user_uid):
    # Debug variable only used for dev purpose
    debug = False

    print("正在转换文件： " + fileName)
    if fileName[0] == "\"":
        fileName = fileName.replace("\"", "")
        if debug:
            print("New file name: " + fileName)

    # Generate DataFrame
    df1 = pd.read_excel(fileName, sheet_name='角色活动祈愿')
    df2 = pd.read_excel(fileName, sheet_name='武器活动祈愿')
    df3 = pd.read_excel(fileName, sheet_name='常驻祈愿')
    df4 = pd.read_excel(fileName, sheet_name='新手祈愿')

    # Rename current columns
    df1.rename(columns={'时间': 'time', '名称': 'name', '类别': 'item_type', '星级': 'rank_type',
                        '总次数': 'total_count', '保底内': 'pity_count', '备注': 'notes'}, inplace=True)
    df2.rename(columns={'时间': 'time', '名称': 'name', '类别': 'item_type', '星级': 'rank_type',
                        '总次数': 'total_count', '保底内': 'pity_count', '备注': 'notes'}, inplace=True)
    df3.rename(columns={'时间': 'time', '名称': 'name', '类别': 'item_type', '星级': 'rank_type',
                        '总次数': 'total_count', '保底内': 'pity_count', '备注': 'notes'}, inplace=True)
    df4.rename(columns={'时间': 'time', '名称': 'name', '类别': 'item_type', '星级': 'rank_type',
                        '总次数': 'total_count', '保底内': 'pity_count', '备注': 'notes'}, inplace=True)

    has_notes_column = False
    for column in df1.columns:
        if column == "notes":
            has_notes_column = True
            if debug:
                print("Notes column found")
    if not has_notes_column:
        print("导出的Excel可能不是来源于最新版Genshin Wish Export，将使用有限的数据进行转换...")
        if debug:
            print("Notes column not found")

    # Modify DF1
    # Add `gacha_type`
    if has_notes_column:
        # Apply corresponding gacha_type for each banner
        df1.loc[df1.notes == '祈愿2', 'gacha_type'] = '400'
        df1.loc[df1.notes.apply(lambda x: True if str(x) == 'nan' else False), 'gacha_type'] = '301'
    else:
        # Apply 301 for all gacha_type
        df1['gacha_type'] = '301'
    # Add `uigf_gacha_type`
    df1['uigf_gacha_type'] = '301'
    # Add `lang`
    df1['lang'] = 'zh-cn'
    # Add `uid`
    df1['uid'] = user_uid
    # Drop `notes` column
    if has_notes_column:
        df1.drop(columns='notes', inplace=True)

    # Modify DF2
    df2['gacha_type'] = 302
    df2['uigf_gacha_type'] = 302
    df2['uid'] = user_uid
    df2['lang'] = 'zh_cn'
    if has_notes_column:
        df2.drop(columns='notes', inplace=True)

    # Modify DF3
    df3['uid'] = user_uid
    df3['lang'] = 'zh_cn'
    df3['gacha_type'] = 200
    df3['uigf_gacha_type'] = 200
    if has_notes_column:
        df3.drop(columns='notes', inplace=True)

    # Modify DF4
    df4['uid'] = user_uid
    df4['lang'] = 'zh_cn'
    df4['gacha_type'] = 100
    df4['uigf_gacha_type'] = 100
    if has_notes_column:
        df4.drop(columns='notes', inplace=True)

    # Merge DF
    MergedDF_list = [df1, df2, df3, df4]
    MergedDF = pd.concat(MergedDF_list)

    # Sort DF
    MergedDF.reset_index(inplace=True)
    MergedDF.drop(columns='index', inplace=True)
    MergedDF.sort_values(by=['time', 'total_count'], ascending=(True, True), inplace=True)

    # Generate ID
    firstID = 1012303100000000000 - MergedDF.shape[0]
    MergedDF['id'] = firstID + MergedDF.index

    # Add `count` and `item_id` column
    MergedDF['count'] = 1
    MergedDF['item_id'] = ''

    # Drop Unused Columns
    MergedDF.reset_index(inplace=True)
    MergedDF.drop(columns='pity_count', inplace=True)

    # Resort Columns
    MergedDF = MergedDF[
        ['count', 'gacha_type', 'id', 'item_id', 'item_type', 'lang', 'name', 'rank_type', 'time', 'uid',
         'uigf_gacha_type']]

    # Reset all cell data type to string
    MergedDF['count'] = MergedDF['count'].astype(str)
    MergedDF['gacha_type'] = MergedDF['gacha_type'].astype(str)
    MergedDF['id'] = MergedDF['id'].astype(str)
    MergedDF['lang'] = MergedDF['lang'].astype(str)
    MergedDF['name'] = MergedDF['name'].astype(str)
    MergedDF['rank_type'] = MergedDF['rank_type'].astype(str)
    MergedDF['time'] = MergedDF['time'].astype(str)
    MergedDF['uid'] = MergedDF['uid'].astype(str)
    MergedDF['uigf_gacha_type'] = MergedDF['uigf_gacha_type'].astype(str)

    # Delete Recent 6 Months Wish History (CST Time)
    if six_month_skip == 'y':
        SHA_TZ = timezone(
            timedelta(hours=8),
            name='Asia/Shanghai',
        )
        utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
        currentCST = utc_now.astimezone(SHA_TZ).replace(tzinfo=None)
        pastSixMonthCST = currentCST + (timedelta(days=-180))
        print("当前时刻180天前的北京时间为：" + str(pastSixMonthCST))
        print("该时间后的记录已放弃，你可以直接使用新的祈愿导出工具合并记录")
        print("完成合并后请仔细该时间点前后的祈愿记录是否有丢失/重复的情况")
        if debug:
            print(datetime.fromisoformat(MergedDF.iloc[0]['time']))
            print(datetime.fromisoformat(MergedDF.iloc[0]['time']) > pastSixMonthCST)
            MergedDF.loc[MergedDF.time.apply(
                lambda x: True if datetime.fromisoformat(x) > pastSixMonthCST else False), 'PastSixMonth'] = 'True'
        MergedDF.drop(MergedDF[MergedDF.time.apply(
            lambda x: True if datetime.fromisoformat(x) > pastSixMonthCST else False)].index, inplace=True)
    else:
        print("导出的祈愿记录包含了近6个月祈愿记录，请注意在未来可能出现记录重复的问题")

    # Output to file
    new_file_name = "uigf_" + str(user_uid) + ".xlsx"
    MergedDF.to_excel(new_file_name, sheet_name='原始数据', index=False)


if __name__ == '__main__':
    print("=" * 20)
    print("Genshin Wish Export UIGF Converter")
    print("版本：1.6")
    print("发布于：https://github.com/Masterain98/genshin-wish-export-uigf-converter")
    print("=" * 20)
    print("本工具用于Genshin Wish Export导出的Excel向UIGF格式转化")
    print("本目录下README.md为使用指南")
    print("完整使用方法请阅读：https://sgdocs.irain.in/FAQ/transfer-from-other-wish-export.html")
    print("=" * 20)
    original_xlsx_name = input("请输入原始Excel文件路径：")
    user_uid_input = input("请输入UID：")
    print("\n" + "*"*5 + " [强烈建议放弃] 近6个月祈愿数据 " + "*"*5)
    print("*" * 5 + " 原因请读取说明文档 " + "*" * 5)
    six_month_skip = input("是否放弃导出近6个月祈愿记录 (Y/N)：").lower()
    while six_month_skip != "y" and six_month_skip != "n":
        six_month_skip = input("是否放弃导出近6个月祈愿记录 (Y/N)：").lower()
    print("=" * 20)
    try:
        converter(original_xlsx_name, user_uid_input)
        input("Excel转换已结束，按任意键退出...")
    except FileNotFoundError:
        input("文件名错误，请尝试将原始Excel修改为较为简单的名称...")
    except Exception as err:
        print("主程序发生意外错误，请联系开发者")
        input(err)
