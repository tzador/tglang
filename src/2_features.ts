import fs from "fs";
import OpenAI from "openai";
import "dotenv/config";

const languages = JSON.parse(fs.readFileSync("src/languages.json").toString());

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

for (const language of languages) {
  if (language === "OTHER") continue;
  if (language === "TL") continue;
  if (language === "FUNC") continue;

  let remapped_language = language;
  if (language === "1S_ENTERPRISE") remapped_language = "1C_ENTERPRISE";
  if (language === "CPLUSPLUS") remapped_language = "C++";
  if (language === "D") remapped_language = "D Programming Language";

  let features: string[] = [];

  for (let i = 0; i < 32; i++) {
    const result = await openai.completions.create({
      prompt: `\
I want to detect the computer language in which a code snippet is written in.
Specifically i want to focus on these languages and write a code snippet classifier for them:
${JSON.stringify(language.slice(1), null, 2)}

I will provide you with one of the languages from the above list,
and you will output a list of 42 small substrings whose occurence in the code snippet is a strong signal for classifying into that language.
Output the list of small substring as JSON list of strings.
Give straight answers only, output only the list of substrings, without any explanations or any other comments.
Include patterns to match keywords, common libraries, operators, punctuation, comments and other kind of tokens and idioms.
Do not output any explanatory comments.

Here is the list of indicative substrings for language '${remapped_language}' as JSON list of strings:
[ "`,

      model: "gpt-3.5-turbo-instruct",
      max_tokens: 3000
    });
    const completion = result.choices[0].text.trim();
    if (!completion) continue;
    try {
      const json = JSON.parse(`[ "` + completion)
        .map((t: string) => t.trim())
        .filter((t: string) => t);
      features.push(...json);
      features = [...new Set(features)].sort();
    } catch {}
  }

  console.log(language, features.length);
  fs.mkdirSync(`data/features`, { recursive: true });
  fs.writeFileSync(
    `data/features/${language}.json`,
    JSON.stringify(features, null, 2)
  );
}
