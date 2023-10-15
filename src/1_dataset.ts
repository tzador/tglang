import fs from "fs";
import OpenAI from "openai";
import sha256 from "sha256";
import "dotenv/config";

const languages = JSON.parse(fs.readFileSync("src/languages.json").toString());

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function generate() {
  for (;;) {
    for (const language of languages) {
      if (language === "OTHER") continue;
      if (language === "TL") continue;
      if (language === "FUNC") continue;

      let remapped_language = language;
      if (language === "1S_ENTERPRISE") remapped_language = "1C_ENTERPRISE";
      if (language === "CPLUSPLUS") remapped_language = "C++";
      if (language === "D") remapped_language = "D Programming Language";

      for (;;) {
        try {
          const snippet_result = await openai.completions.create({
            prompt: `\
I want you to generate a code snippet in programming language (or markup language) '${remapped_language}'.
Give straight answers only, output just the code snippet and nothing else.
The code snippet should be long and complex.
The output should be in annotated markdown code snippet.
Do not print any explanations, just the code in triple backticks.
The code snippet is:
\`\`\`${language}`,

            model: "gpt-3.5-turbo-instruct",
            max_tokens: 3000,
            stop: ["```"]
          });
          const snippet = snippet_result.choices[0].text.trim();
          if (!snippet) continue;

          const check_result = await openai.completions.create({
            prompt: `\
\`\`\`
${snippet}
\`\`\`

The above snippet is written in '${language}', ie is it syntactically correct in '${remapped_language}'? (yes/no):`,

            model: "gpt-3.5-turbo-instruct",
            max_tokens: 100,
            stop: ["es", "o"]
          });
          const answer = check_result.choices[0].text.trim().toLowerCase();
          const yes = answer.startsWith("y");

          if (!yes) continue;

          console.log(">>>>", language);
          console.log(snippet);
          console.log(">>", answer);

          fs.mkdirSync(`data/snippets/${language}`, { recursive: true });
          fs.writeFileSync(
            `data/snippets/${language}/${sha256(snippet)}.txt`,
            snippet
          );
          break;
        } catch {
          continue;
        }
      }
    }
  }
}

for (let i = 0; i < 32; i++) generate();
