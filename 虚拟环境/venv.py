'''
创建虚拟环境
指令中，env1是虚拟环境名称，可以自定义；python=3.9.13是指定python版本，可以自定义
'''
conda create -n env1 python=3.9.13


# 激活虚拟环境  
conda activate env1  


'''
安装第三方库
env1是待安装第三方库的虚拟环境名称，numpy是待安装的第三方库  
'''
conda install -n env1 numpy  

# 退出该虚拟环境并回到基础base环境
conda deactivate

# 删除虚拟环境  
conda env remove -n env1

# 或者  
conda remove -n env1 --all


# 查看当前环境下已安装的第三方库：
conda list  

# 查看指定环境下已安装的第三方库：
conda list -n env1 

# 更新指定环境的第三方库：
conda update -n env1 numpy

# 删除指定环境的第三方库：
conda remove -n env1 numpy  

# 查看全部虚拟环境：
conda info -e  
# 或者  
conda env list 

# 更新全部第三方库
conda update --all


# 安装requirements.txt中的库
pip install -r requirements.txt

# 基于venv管理虚拟环境
# 创建虚拟环境（其中 F:\py_env\env2 是虚拟环境路径）  
>>>python -m venv F:\py_env\env2  
  
# 激活虚拟环境（运行 激活脚本）  
>>>F:\py_env\env2\Scripts\activate  
  
# 安装、更新、删除第三库方法同常规  
>>>pip install plotly  
>>>pip install --upgrade plotly  
>>>pip uninstall plotly  
  
# 退出虚拟环境  
>>>deactivate  
  
# 删除虚拟环境（最简单可以直接删除虚拟环境文件夹）  


