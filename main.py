import pandas as pd


def converter(fileName, user_uid):
    print("Converting " + fileName)

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

    # Modify DF1
    # Add `gacha_type`
    df1.loc[df1.notes == '祈愿2', 'gacha_type'] = '400'
    df1.loc[df1.notes.apply(lambda x: True if str(x) == 'nan' else False), 'gacha_type'] = '301'
    # Add `uigf_gacha_type`
    df1['uigf_gacha_type'] = '301'
    # Add `lang`
    df1['lang'] = 'zh-cn'
    # Add `uid`
    df1['uid'] = user_uid
    # Drop `notes` column
    df1.drop(columns='notes', inplace=True)

    # Modify DF2
    df2['gacha_type'] = 302
    df2['uigf_gacha_type'] = 302
    df2['uid'] = user_uid
    df2['lang'] = 'zh_cn'
    df2.drop(columns='notes', inplace=True)

    # Modify DF3
    df3['uid'] = user_uid
    df3['lang'] = 'zh_cn'
    df3['gacha_type'] = 200
    df3['uigf_gacha_type'] = 200
    df3.drop(columns='notes', inplace=True)

    # Modify DF4
    df4['uid'] = user_uid
    df4['lang'] = 'zh_cn'
    df4['gacha_type'] = 100
    df4['uigf_gacha_type'] = 100
    df4.drop(columns='notes', inplace=True)

    # Merge DF
    MergedDF_list = [df1, df2, df3, df4]
    MergedDF = pd.concat(MergedDF_list)

    # Sort DF
    MergedDF.reset_index(inplace=True)
    MergedDF.drop(columns='index', inplace=True)
    MergedDF.sort_values(by=['time', 'total_count'], ascending=(True, True), inplace=True)

    # Generate ID
    firstID = 1612303100000000000 - MergedDF.shape[0]
    MergedDF['id'] = firstID + MergedDF.index

    # Add `count` and `item_id` column
    MergedDF['count'] = 1
    MergedDF['item_id'] = ''

    # Drop Unused Columns
    MergedDF.reset_index(inplace=True)
    MergedDF.drop(columns='pity_count', inplace=True)

    # Resort Columns
    MergedDF = MergedDF[['count', 'gacha_type', 'id', 'item_id', 'item_type', 'lang', 'name', 'rank_type', 'time', 'uid',
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

    # Output to file
    new_file_name = "uigf_" + str(user_uid) + ".xlsx"
    MergedDF.to_excel(new_file_name, sheet_name='原始数据', index=False)


if __name__ == '__main__':
    original_xlsx_name = input("请输入原始Excel文件路径：")
    user_uid_input = input("请输入UID：")
    converter(original_xlsx_name, user_uid_input)
    input("Program ended...")
