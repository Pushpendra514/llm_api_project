with open("question.json","w") as fin:
    fin.write(data["choices"][0]["message"]["content"])