# genshin-wish-export-uigf-converter
A Python tool to convert genshin-wish-expoert data to UIGF format

将 [genshin-wish-expoert](https://github.com/biuuu/genshin-wish-export) 的数据转化为 [UIGF](https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat) 格式

## ID生成

- 第一次祈愿的ID记为 `1012303100000000000 - 记录的总祈愿次数`
- 此后每条祈愿记录ID顺次`+1`

## 使用方法

1. 运行程序
2. 拖入`genshin-wish-expoert`导出的Excel文件，或者手动输入该文件的路径（同目录下只需输入该文件的文件名）
3. 输入你的游戏 UID
4. 选择是否放弃近6个月的祈愿记录
   1. 如果不放弃，则在使用新的祈愿导出工具时会出现祈愿记录重复的情况
   2. 如果放弃，请在使用新的祈愿导出工具时获取全部祈愿记录，并手动检查对应时间点前后是否有数据重复/丢失
5. 等待程序运行完成

![](https://github.com/Masterain98/genshin-wish-expoert-uigf-converter/blob/main/how_to_use.gif?raw=true)

## 截图

![](https://github.com/Masterain98/genshin-wish-expoert-uigf-converter/blob/main/screenshot1.png?raw=true)

![](https://github.com/Masterain98/genshin-wish-expoert-uigf-converter/blob/main/screenshot2.png?raw=true)
