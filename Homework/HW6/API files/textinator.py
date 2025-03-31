"""
Author: <NAME>
Purpose: Load files, loads stopwords, does wordcount, sentiment analysis,
anything that we want to visualize in the visionator
Output:
"""

from collections import defaultdict, Counter
from pdfminer.high_level import extract_text
import json
import os
import re
from myopenai import MyOpenAPI
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import dotenv
import pandas as pd
import vaderSentiment.vaderSentiment as vs
from SANKEY import show_sankey
import gensim.corpora as corpora
import pickle
import gensim
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import seaborn as sns
import pyLDAvis.gensim_models
import pyLDAvis


dotenv.load_dotenv()
api = MyOpenAPI()

class Textinator:
    def __init__(self):
        """ Constructor
        datakey --> (filelabel --> datavalue)
        """
        self.data = defaultdict(dict)
        self.stop_list = list()

    def load_text(self, filename, label=None, parser=None, GPT = False):
        """ Register a document with the framework.
        Extract and store data to be used later by
        the visualizations """

        if parser is None:
            if GPT:
                results = self.default_parser(filename, GPT = True)
            else:
                results = self.default_parser(filename, GPT = False)
        else:
            if GPT:
                results = parser(filename, GPT = True)
            else:
                results = parser(filename, GPT = False)


        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v

    def filter_words(self, words):
        """Given a list of words, removes all specified characters from each
        word and removes any words that, following the filtering, are not
        exclusively letters (isalpha), are in the stop words list, or are
        less than 3 characters"""

        # Creation of translation table to remove characters
        translation_table = str.maketrans(
            {"\n": "", "\t": "", "\r": "", "=": "",
             ",": "", "-": "", "(": "", ")": "",
             ".": "", ":": "", "?": "", ";": "", "[": "", "]": "", " ": ""})

        cleaned_words = []
        # Loop iterating through words, applying translate() and lowercase()
        for i in words:
            i = i.translate(translation_table)
            i = i.lower()
            # Conditional statement checking filtering conditions
            if i not in self.stop_list and i.isalpha() and len(i) > 2:
                cleaned_words.append(i)
        lemmatizer = WordNetLemmatizer()
        final_words = []
        for i in cleaned_words:
            final_words.append(lemmatizer.lemmatize(i))

        return final_words

    def json_parser(self, filename):
        f = open(filename)
        raw = json.load(f)
        text = raw['text']
        words = text.split(" ")
        wc = Counter(words)
        num = len(words)
        return {'wordcount': wc, 'numwords': num}

    def GPT_key_sections(self, text, filename):
        """Given a text, calls the GPT API and prompts it to locate and rewrite
        the most important portions of the text to a new file."""
        # Gets the filename of the text
        base_name = os.path.splitext(os.path.basename(filename))[0]

        # Generates the name of the file for the GPT output and the prompt
        output_name = f'data/GPT_sectioned/{base_name}.txt'
        prompt = """Find the sections of this text that really contribute to\
        its meaning. Example: find the abstract, key defining sentences,\
        discussion, and conclusion of a research paper. Only return exactly\
        what the article says. TEXT: """
        prompt += text

        # Calls GPT API and formats output
        response_text = api.ask(prompt=prompt)
        response_text = re.sub(r"\*\*.*?\*\*", '', response_text)
        response_text = re.sub(r"-", '', response_text)
        # Writes output to the specified file
        with open(output_name, 'w') as file:
            file.write(response_text)

    def default_parser(self, filename, GPT = False):
        """ Parse a standard text file and produce
        extract data results in the form of a dictionary. """

        base_name = os.path.splitext(os.path.basename(filename))[0]
        base_file = re.sub(r'_\d+$', '', base_name)
        output_name = f'data/converted_files/{base_file}/{base_name}.txt'
        raw_text = []
        with open(filename, 'r') as file:
            text = file.read()
            if GPT:
                self.GPT_key_sections(text, filename)
            for i in file:
                raw_text.append(i.split(" "))
        raw_text = [i for lst in raw_text for i in lst]
        cleaned_words = self.filter_words(raw_text)

        with open(output_name, 'w') as file:
            file.write(text)

        # Gets word counts in a Counter datatype
        wc = Counter(cleaned_words)
        num = len(cleaned_words)

        return {'wordcount': wc, 'numwords': num}

    def pdf_parser(self, filename, GPT = False):
        """Called to parse a PDF file. Extracts text. Uses a PDF library
        to extract text, calls filter_word() to clean the output, and outputs
        the cleaned words in the dictionary counter datatype. Also writes the
        most important parts of the text to separate files using GPT API"""
        base_name = os.path.splitext(os.path.basename(filename))[0]
        base_file = re.sub(r'_\d+$', '', base_name)
        output_name = f'data/converted_files/{base_file}/{base_name}.txt'

        text = extract_text(filename)
        # Writes most important portions of text to separate files using GPT
        if GPT:
            self.GPT_key_sections(text, filename)
        with open(output_name, 'w') as file:
            file.write(text)

        # Filters words
        cleaned_words = self.filter_words(text.split(" "))

        # Gets word counts in a Counter datatype
        wc = Counter(cleaned_words)
        num = len(cleaned_words)

        return {'wordcount': wc, 'numwords': num}

    def load_stop_words(self, stopwords_file):
        """Loads stopwords from a text file"""
        with open(stopwords_file) as infile:
            for i in infile:
                self.stop_list.append(i.strip())

    def ASBA_scores(self, filename, aspect_list):
        """"""
        base_name = os.path.splitext(os.path.basename(filename))[0]
        output_name = f'results/ASBA/{base_name}.csv'
        with open(filename, "r") as file:
            text = file.read()

        # Load the ABSA model and tokenizer
        model_name = "yangheng/deberta-v3-base-absa-v1.1"
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        classifier = pipeline("text-classification", model=model,
                              tokenizer=tokenizer, device = 'mps')

        result = {}
        for aspect in aspect_list:
            result[aspect] = classifier(text, text_pair=aspect)[0]
        df = pd.DataFrame.from_dict(result, orient='index')
        df.to_csv(output_name)
        return df

    def wordcount_sankey(self, word_list = None, k = 5):
        """Given a list of words and a number of top most common words to be
        found from the text stored as state variables within the class,
        generates a sankey diagram using including either the words in the list
        passed to the function, or, if no list was passed, the union of the
        k most common words from each text in the class."""

        # Creates two empty dataframes
        word_counts = pd.DataFrame()
        stacked_df = pd.DataFrame()

        # Conditional statement to find the k most common words if no list
        # is passed
        if word_list is None:
            word_list = set()

            # Loop creating a list of the union of the k most common words
            # from each text.
            for text in self.data["wordcount"]:
                word_list = word_list.union(
                set(i[0] for i in self.data["wordcount"][text].most_common(k)))
            # Converts the set of all most common words into a sorted list
            word_list = list(word_list)
            word_list.sort()

            # Loop iterating through all the texts in the class and saving
            # the text name and word frequencies for all the most common
            # words to a dataframe.
            for text in self.data["wordcount"]:
                word_counts["Words"] = word_list
                word_counts["Text"] = text
                word_counts["Frequency"] = list(self.data[
                                "wordcount"][text][word] for word in word_list)
                # Adds each separate dataframe from each text to a singular
                # dataframe (stacked format for sankey plotting)
                stacked_df = pd.concat([
                    stacked_df, word_counts], ignore_index=True, sort=False)
        # Conditional else statement for if a list of words has been passed
        else:
            # Loop iterating through all texts in the class, saving the text
            # name and word frequencies for all words in the word list param
            for text in self.data["wordcount"]:
                word_counts["Words"] = word_list
                word_counts["Text"] = text
                word_counts["Frequency"] = list(self.data[
                                "wordcount"][text][word] for word in word_list)
                # Concatenates separate dataframes for each text to one df
                stacked_df = pd.concat([
                    stacked_df, word_counts], ignore_index=True, sort=False)
        # Generates and displays sankey
        show_sankey(stacked_df, "Text", "Words", vals = "Frequency")

    def sentiment_analysis(self):
        """Generates sentiment scores for each text using VADER library
        to get a score for each word and average those scores across each
        text."""

        total_sentiment = []
        text_sentiments = []
        # Creates the sentiment analyzer object from the library
        analyzer = vs.SentimentIntensityAnalyzer()

        # Loop iterating through all texts in the class
        for text in self.data["wordcount"]:
            # Iterates through each word in the text
            for i in self.data["wordcount"][text].keys():
                # Adds the polarity score from the analyzer for that word
                # multiplied by the number of times the word appears to new list
                total_sentiment.append(analyzer.polarity_scores(i)[
                                "compound"] * self.data["wordcount"][text][i])
            # Averages text sentiment scores for the whole text
            if self.data["numwords"][text] == 0:
                self.data["numwords"][text] = 0.0000001

            text_sentiments.append(sum(total_sentiment) / self.data[
                                                            "numwords"][text])
    def dot_plot_df(self):
        df_list = []
        for filename in os.listdir("results/ASBA"):
            df = pd.read_csv(f'results/ASBA/{filename}')
            df['file'] = os.path.splitext(os.path.basename(filename))[0]
            df_list.append(df)
        df = pd.concat(df_list, ignore_index=True)
        df.rename(columns={"Unnamed: 0": 'topic'}, inplace=True)
        return df


    def LDA(self, num_topics_per_document, passes):
        for directory in os.listdir("data/converted_files/"):
            full_directory = os.path.join("data/converted_files", directory)
            text_list = []

            for filename in os.listdir(full_directory):
                full_filename = os.path.join(f'data/converted_files/{directory}', filename)
                with open(full_filename, "r") as file:
                    text = file.read()
                text = text.strip().split()
                text = self.filter_words(text)
                text_list.append(text)

            dictionary = corpora.Dictionary(text_list)

            corpus = [dictionary.doc2bow(text) for text in text_list]

            # !!! PICKLE THE CORPUS !!!
            pickle.dump(corpus, open('corpus.pkl', 'wb'))

            ldamodel = gensim.models.ldamodel.LdaModel(corpus,
                                                       num_topics=num_topics_per_document,
                                                       id2word=dictionary,
                                                       passes=passes)

            vis = pyLDAvis.gensim_models.prepare(ldamodel, corpus, dictionary)
            pyLDAvis.save_html(vis, f'lda_visualization{directory}.html')

            data = ldamodel.show_topics(num_topics=num_topics_per_document)
            topics = []
            for topic_id, keywords in data:
                words = []
                weights = []
                for item in keywords.split(" + "):
                    weight, word = item.split("*")
                    weights.append(float(weight))
                    words.append(word.strip('"'))
                topics.append((topic_id, words, weights))

            # Create subplots
            num_topics = len(topics)
            fig, axes = plt.subplots(1, num_topics, figsize=(15, 5), sharey=True)

            for i, (topic_id, words, weights) in enumerate(topics):
                axes[i].barh(words, weights, align='center')
                axes[i].set_title(f"Topic {topic_id}")

            # Adjust layout
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()



    def create_dot_plot(self, df):
        print(df)
        plt.figure(dpi=500)
        plt.size = (12, 10)

        color_labels = {"Positive": "red", "Negative": "blue",
                        "Neutral": "grey"}
        df["color"] = df["label"].map(color_labels)

        sns.scatterplot(
            data=df,
            x='file',  # X-axis is the 'label' column
            y='topic',  # Y-axis is the DataFrame identifier
            size='score',  # Dot size is proportional to 'score'
            hue='label',  # Dot color represents the 'label'
            palette=color_labels,
            legend='brief'
        )

        # Customize the plot
        plt.title("Sentiment and Confidence Score per Category", fontsize=10)
        plt.xlabel("Paper Type", fontsize=10)
        plt.ylabel("Topic", fontsize=10)
        plt.xticks(rotation=90)  # Rotate X-axis labels for readability

        # Adjust legend
        plt.legend(title="Labels", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()