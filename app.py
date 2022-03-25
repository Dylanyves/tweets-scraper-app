import streamlit as st
import pandas as pd
from machine import Machine
from data import Data
from train import Train
import plotly.express as px

st.set_page_config(
    page_title='Tweets Scraper',
    layout="wide"
)

class App:
    def header():
        st.title('Tweets Scraper & Analyser')
        st.markdown('***')

    def sidebar():
        years = [int(2024-i) for i in range(1, 17)]
        with st.sidebar:
            st.header('Input Form')
            st.caption('You can leave either username or key word blank')
            with st.form('form'):
                input_username = st.text_input('Username')
                input_key_word = st.text_input('Key Word')
                input_year_before = st.selectbox('Tweets before year', years)
                input_year_after = st.selectbox('Tweets since year', years)
                input_size = st.slider('Tweets limit', 10, 10000)
                submit_btn = st.form_submit_button('Scrape!') 

            if submit_btn:
                input_dict = {
                        'username':input_username.strip(),
                        'key':input_key_word.strip(),
                        'year_before':input_year_before,
                        'year_after':input_year_after,
                        'size':input_size,
                    }
                if input_username:
                    try:
                        with st.spinner('Wait for it...'):
                            pcc = Machine(input_dict)
                            result = pcc.run()

                            # Save the result to session storage
                            st.session_state['tweets'] = result
                            st.session_state['size'] = input_size
                        st.success('Done!')
                    except ValueError:
                        st.error('Username not found!')
                elif input_key_word:
                    with st.spinner('Wait for it...'):
                        pcc = Machine(input_dict)
                        result = pcc.run2()

                        # Save the result to session storage
                        st.session_state['tweets'] = result
                        st.session_state['size'] = input_size
                    st.success('Done!')
                else: 
                    st.error('Fill in the form!')



    def content_1():
        col1, col2 = st.columns((2, 1))
        with col1:
            try:
                all_tweets = st.session_state.tweets[:st.session_state.size]
                data = Data(all_tweets)

                # Total tweets
                st.write('Total tweets:', len(all_tweets))   

                # Dates
                dates = data.get_dates()
                st.write('From', dates[-1], 'to', dates[0])        

                st.markdown('***')     

                # Most liked tweet
                most_liked_tweet = data.get_most_liked_tweet()
                st.subheader('Most liked tweet')
                st.caption(f'{most_liked_tweet.datetime}')
                st.write(most_liked_tweet.tweet)
                st.caption(f'**{most_liked_tweet.likes_count} likes**')

                # Most retweeted tweet
                most_retweeted_tweet = data.get_most_retweeted_tweet()
                st.subheader('Most retweeted tweet')
                st.caption(f'{most_retweeted_tweet.datetime}')
                st.write(most_retweeted_tweet.tweet)
                st.caption(f'**{most_retweeted_tweet.retweets_count} retweets**')

                # Most replied tweet
                most_replied_tweet = data.get_most_replied_tweet()
                st.subheader('Most replied tweet')
                st.caption(f'{most_replied_tweet.datetime}')
                st.write(most_replied_tweet.tweet)
                st.caption(f'**{most_replied_tweet.retweets_count} replies**')

            except ValueError:
                st.info('No data to be displayed')
            except TypeError:
                st.info('No data to be displayed')
            except AttributeError:
                st.info('No data to be displayed')
            except IndexError:
                st.info('No data to be displayed')

        
        with col2:
            with st.expander('Example', expanded=True):
                st.caption('Input Example')
                st.code('''Username = "elonmusk" \nKeyWord = "tesla" \nTweetsBeforeYear = 2021 \nTweetsSinceYear = 2018''')
                st.markdown('With these inputs, the machine will take all tweets from **@elonmusk** that contains the word **tesla** from the year **2018** to **2020**')
            with st.expander('Info', expanded=True):
                st.markdown('Created using **streamlit** and **twint**')

        st.markdown('***')

    def content_2():
        col1, col2 = st.columns(2)
        try:
            all_tweets = st.session_state.tweets[:st.session_state.size]
            data = Data(all_tweets)

            with col1:
                # Hashtags info
                st.subheader('Hashtags')
                _, has_tags = data.count_tags()
                pct_tags = round(((has_tags / len(all_tweets)) * 100), 1)
                tags_df, _ = data.get_tags_mentions_dataframes()
                st.write(pct_tags, 'percent tweets contain hashtags')
                if len(tags_df) >= 1:
                    st.write(f'**#{tags_df.loc[0].Hashtag}** is the most used tag')
                else: st.write(None)
                st.write(tags_df)
                st.caption('Hashtags list')

            with col2:
                # Mentions info
                st.subheader('Mentions')
                _, has_mentions = data.count_mentions()
                pct_mentions = round(((has_mentions / len(all_tweets)) * 100), 1)
                _, mentions_df = data.get_tags_mentions_dataframes()
                st.write(pct_mentions, 'percent tweets mention someone')
                if len(mentions_df) >= 1:
                    st.write(f'User **@{mentions_df.loc[0].Mention}** being mentioned the most')
                else: st.write(None)
                st.write(mentions_df)
                st.caption('Mentions list')

            st.markdown('***')
        except AttributeError:
            # If no tweets
            print('No data to be displayed')
        except ZeroDivisionError:
            st.info('No data to be displayed')

    def content_3():
        try:
            all_tweets =  [x.tweet for x in st.session_state.tweets[:st.session_state.size]]
            all_dates = [x.datetime.split(' ')[0] for x in st.session_state.tweets[:st.session_state.size]]
            df = pd.DataFrame({'date':all_dates, 'tweet':all_tweets})
            predicted_table = Train(df.copy()).run_all()
            st.subheader('Sentiment Analysis')
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric('Average Polarity', round(predicted_table.polarity.mean(), 3))
            with col2:
                st.metric('Average Subjectivity', round(predicted_table.subjectivity.mean(), 3))
            with col3:
                st.metric('Negative Tweets', len(predicted_table[predicted_table.sentiment == str(-1)]))
            with col4:
                st.metric('Neutral Tweets', len(predicted_table[predicted_table.sentiment == str(0)]))
            with col5:
                st.metric('Positive Tweets', len(predicted_table[predicted_table.sentiment == str(1)]))

            box_1, box_2 = st.columns(2)
            with box_1:
                b1 = px.box(predicted_table, x='polarity', title='Polarity Distribution')
                st.plotly_chart(b1, use_container_width=True)
            with box_2:
                b2 = px.box(predicted_table, x='subjectivity', title='Subjectivity Distribution')
                st.plotly_chart(b2, use_container_width=True)

            dist_1, dist_2 = st.columns(2)
            with dist_1:
                pie = px.pie(predicted_table, names='sentiment', hole=.3, title='Sentiment Distribution')            
                st.plotly_chart(pie, use_container_width=True)
                st.caption('-1 = Negative, 0 = Neutral, 1 = Positive')
            with dist_2:
                hist = px.histogram(predicted_table, x='sentiment')
                st.plotly_chart(hist, use_container_width=True)

            scatter = px.scatter(predicted_table, x=predicted_table.subjectivity, y=predicted_table.polarity, color=predicted_table.subjectivity, title='Tweets Polarity and Subjectivity Relationship')
            st.plotly_chart(scatter, use_container_width=True)

            st.markdown('***')

            with st.expander('Full Data', expanded=False):
                predicted_table.tweet = all_tweets
                st.table(predicted_table)


        except ZeroDivisionError:
            # If no tweets
            print('No data to be displayed')
        except AttributeError:
            # If no tweets
            print('No data to be displayed')


    def app():
        App.header()
        App.sidebar()
        App.content_1()
        App.content_2()
        App.content_3()


if __name__ == '__main__':
    app = App
    app.app()