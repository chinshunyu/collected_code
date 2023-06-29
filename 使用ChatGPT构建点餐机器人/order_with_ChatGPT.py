import panel as pn  # GUI
pn.extension()
import os
import openai

openai.api_key = 'sk-xxx'

def get_completion(prompt, model = 'gpt-3.5-turbo'):
    messages = [{'role':'user','content':prompt}]
    response = openai.ChatCompletion.create(model = model,
                                            messages = messages,
                                            temperature = 0, # 控制模型输出的随机程度
                                            )
    return response.choices[0].message['content']

def get_completion_from_messages(messages, model = 'gpt-3.5-turbo', temperature = 0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message['content']

# messages = [
#     {'role':'system', 'content':'You are an assistant that speaks like Shakespeare.'},
#     {'role':'user','content':'tell me a joke.'},
#     {'role':'assistant', 'content':'I don\'t know'}
# ]
# response = get_completion_from_messages(messages,temperature=1)
# print(response)

def collect_messages(_):
    '''
    订餐机器人
    '''
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)


panels = [] # collect display 

context = [{'role':'system', 'content':"""
你是订餐机器人，为可达鸭餐厅自动收集订单信息。
你要首先问候顾客。然后等待用户回复收集订单信息，包括餐品和数量。如果用户没有说数量，你要问下。
收集完信息需确认顾客是否还需要添加其他内容。
最后需要询问是否自取或外送，如果是外送，你要询问地址并告诉用户配送费是8块。
最后告诉顾客订单总金额，并送上祝福。

请确保明确所有选项、附加项和尺寸，以便从菜单中识别出该项唯一的内容。
你的回应应该以简短、非常随意和友好的风格呈现。

菜单包括：

主食：
鸡排堡（大、中、小） 12.95、10.00、7.00
鸡腿堡（大、中、小） 10.95、9.25、6.50
嫩牛堡（大、中、小） 19.95、15.75、10.75
鸡肉卷（大、中、小） 11.95、9.75、6.75

小食：
薯条（大、小） 4.50、3.50
希腊沙拉 7.25
香肠 3.00
加拿大熏肉 3.50

配料：
奶酪 2.00
蘑菇 1.50
AI酱 1.50
辣椒 1.00

饮料：
可乐（大、中、小） 3.00、2.00、1.00
雪碧（大、中、小） 3.00、2.00、1.00
农夫山贼矿泉水 5.00
"""} ]  # accumulate messages


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)