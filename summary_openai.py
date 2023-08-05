import openai

# from summary_openai import summarize_article
# self.summary = summarize_article(self.content)

with open("openai_key.txt", "r") as file:
    openai_key = file.readline().strip()


def summarize_article(article_text):
    print(article_text)
    # Initialize the OpenAI API client with your API key
    openai.api_key = openai_key

    # Define the prompt for GPT-4
    prompt_text = f" Summarize the below article  in the form of 5 key takeaways as bullets. Write it in simple english and use an informative and fun writing style: {article_text}"

    message = [{"role": "user", "content": prompt_text}]

    # Request a completion from GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.1,
        max_tokens=500,  # Adjust based on your preference for summary length
    )

    # Extract the generated summary
    summary = response.choices[0].message.content.strip()

    return summary
