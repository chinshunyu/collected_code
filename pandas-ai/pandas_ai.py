import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

df = pd.DataFrame({
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "gdp": [19294482071552, 2891615567872, 2411255037952, 3435817336832, 1745433788416, 1181205135360, 1607402389504, 1490967855104, 4380756541440, 14631844184064],
    "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.4, 7.23, 7.22, 5.87, 5.12]
})


llm = OpenAI(api_token='sk-xxx')

pandas_ai = PandasAI(llm)
pandas_ai.run(df, prompt='Which are the 5 happiest countries?')
pandas_ai.run(df, prompt='What is the sum of the GDPs of the 2 unhappiest countries?')
pandas_ai.run(
    df,
    "Plot the histogram of countries showing for each the gpd, using different colors for each bar",
)