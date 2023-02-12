declation=$1
echo 当前目录是：%cd%
echo;

echo 开始添加变更：git add .
git add .
echo;

set /p declation=输入提交的commit信息:
git commit -m "${declation}"
echo;

git push


echo 执行完毕！
echo;
