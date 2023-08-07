import pandas as pd

df = pd.DataFrame(columns=['date', 'name', 'message'])

with open('hakuna_madata.txt', 'r', encoding='utf-8') as file:
    for line in file:
        if ':' in line:
            print(line)
            try:
                date, message_block = line.split('-', 1)
                name, message = message_block.split(':', 1)
                df.loc[len(df)] = [date, name, message.replace('\n', '')]

            except:
                continue

df.to_csv('hakuna_madata.csv', index=False)
