# genshin-wish-expoert-uigf-converter
A Python tool to convert genshin-wish-expoert data to UIGF format

将 [genshin-wish-expoert](https://github.com/biuuu/genshin-wish-export) 的数据转化为 [UIGF](https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat) 格式

## ID生成

- 第一次祈愿的ID记为 `1612303100000000000 - 记录的总祈愿次数`
- 此后每条祈愿记录ID顺次`+1`

## 使用方法

1. 运行程序
2. 拖入`genshin-wish-expoert`导出的Excel文件，或者手动输入该文件的路径（同目录下只需输入该文件的文件名）
3. 等待程序运行完成
