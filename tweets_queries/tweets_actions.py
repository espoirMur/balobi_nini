
def tweet_words_count(client, word_count_path):
    """
    this function should tweet the word_count

    Args:
        client ([type]): [description] this  is the tweet client
        word_count_path ([type]): [description] path to the image to  tweet
    """
    message = """
    Here are the most used words by Congolese on twitter today...
    Voici les mots qui ont été utilisé par les Congolais sur twitter aujourd'hui
    #RDC #DRC #RDCongo
    """
    client.update_with_media(word_count_path, message)

