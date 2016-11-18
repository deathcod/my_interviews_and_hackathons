<?php

ini_set('display_errors', 1);
require_once('TwitterApi.php');

class TwitterApiFunctions
{
    /**
     * TwitterApi Instance
     */
    private $twitterApiInstance;

    /**
     * Create the instance of TwitterApi by passing all the required keys for authentication.
     * These are all available by creating your own application on https://apps.twitter.com/
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *
     */
    public function __construct()
    {
        $keys = array(
            'oauth_access_token'        => "788273630945742849-ghgqY1rsJVeYLBCQZ0IuHfUjz3ejTe1",
            'oauth_access_token_secret' => "kxuZpgWPjyTVYscJKFml2RI2nvjBRVND4qg878gPEePq9",
            'consumer_key'              => "slAIp8kYfqM4yjEm7G8hzJJo8",
            'consumer_secret'           => "kBBNIMiEdLYGTiJt7Lt3oZP52G2X8jM8Os1u82VXs2u1Ape1WN" 
            );

        $this->twitterApiInstance = new TwitterApi($keys);
    }

    /**
     * GET search/tweets
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *
     * @param array of query parameter to be submitted with the url.
     *
     * @return string json, list of tweets
     *
     * @see https://dev.twitter.com/rest/reference/get/search/tweets
     */
    public function searchTweets($getfield)
    {
        $tweets =  $this->twitterApiInstance
                  ->setUrlwithExtension("search/tweets.json")
                  ->setGetParameters($getfield)
                  ->buildOauth()
                  ->makeRequest();

        $tweets     = json_decode($tweets);
        $tweets     = $this->arrayCastRecursive($tweets);
        $tweets     = $tweets['statuses'];

        return $tweets;
    }

    /**
     * Here a single tweet is checked on the conditions passed in $tweet_keys, if a tweet doesnot 
     * satisfies any one of the conditions "False" is returned else "True"
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *  
     * @param array :: $tweet, a single tweet
     * @param array :: $tweet_keys, array of conditions
     *
     * @return boolean :: True, if all conditions are satisfied, else False 
     */
    public function getSingleRefineTweet($tweet , $tweet_keys)
    {
        foreach ($tweet_keys as $key => $value)
        {
            switch ($key)
            {
                case 'retweet_count':

                    foreach($value as $comparators => $comp_value )
                    {
                        switch ($comparators) 
                        {
                            case 'greater':
                                if( !($tweet['retweet_count'] > $comp_value))
                                    return false;
                                break;

                            case 'less':
                                if( !($tweet['retweet_count'] < $comp_value))
                                    return false;
                                break;
                            
                            case 'greaterEqual':
                                if( !($tweet['retweet_count'] >= $comp_value))
                                    return false;
                                break;

                            case 'lessEqual':
                                if( !($tweet['retweet_count'] <= $comp_value))
                                    return false;
                                break;

                            case 'equal':
                                if( !($tweet['retweet_count'] == $comp_value))
                                    return false;
                                break;

                            case 'notEqual':
                                if( !($tweet['retweet_count'] != $comp_value))
                                    return false;
                                break;
                        }
                    }
                    break;

                // add more conditions 
            }
        }
        return True;
    }
    /**
     * Here for each tweet in the array of tweets, check if it pass the condtion, if yes add the 
     * tweet into a new array named $newRefineTweets
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *
     * @param array :: $tweets, array of tweets
     * @param array :: $tweet_keys, array of conditions
     *
     * @return array :: $newRefineTweets, array of tweets that fullfills the conditions
     */
    public function getRefineTweets($tweets, $tweet_keys)
    {
        $newRefineTweets = array();
        foreach ($tweets as $tweetValue)
        {
            if($this->getSingleRefineTweet($tweetValue , $tweet_keys))
            {
                $newRefineTweets[] = $tweetValue;
            }
        }

        return $newRefineTweets;
    }

    /**
     * Takes a stdclass object or array of stdclass object and convert them to all to array type 
     * recursively.
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *
     * @param array :: $stdClassToArray, stdClass object or array of stdClass objects 
     *
     * @return array :: object of type array is returned.
     */
    public function arrayCastRecursive($stdClassToArray)
    {
        if (is_array($stdClassToArray)) 
        {
            foreach ($stdClassToArray as $key => $value) 
            {
                if (is_array($value)) 
                {
                    $stdClassToArray[$key] = $this->arrayCastRecursive($value);
                }
                if ($value instanceof stdClass) 
                {
                    $stdClassToArray[$key] = $this->arrayCastRecursive((array)$value);
                }
            }
        }
        if ($stdClassToArray instanceof stdClass) 
        {
            return $this->arrayCastRecursive((array)$stdClassToArray);
        }
        return $stdClassToArray;
    }
}
?>
