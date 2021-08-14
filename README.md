# greek-vowel-patterns

Modern Greek contains multiple phoneme sounds which can be written in different ways ([single-letter vowels](https://en.wikiversity.org/wiki/Greek_Language/Vowels), [double-letter vowels](https://en.wikiversity.org/wiki/Greek_Language/Two-letter_Vowels)). In particular:
1. "ee" can be written 6 ways: ι, η, υ, ει, οι, υι
2. "eh" can be written 2 ways: ε, αι
3. "oh" can be written 2 ways: ο, ω

This repository finds patterns in the occurrences of these otherwise indistinguishable vowel sounds, which will hopefully be of help to first-time Greek language learners.

Raw Greek-language token were acquired from the [Europarl dataset](https://opus.nlpl.eu/Europarl.php) containing 44.1M tokens.

(Initially attempted to acquire word/frequency data from the [elTenTen](https://www.sketchengine.eu/eltenten-greek-corpus/) Greek webcrawl dataset via [SketchEngine](https://www.sketchengine.eu/), but encountered limitations on what data could be downloaded without email correspondences and payments.)

Specific question we wish to answer here:
1. For a given phoneme, how common is each written representation?
2. For a given phoneme, conditioning on the preceding letter, how common is each written representation?
3. For a given phoneme, conditioning on the following letter, how common is each written representation?
