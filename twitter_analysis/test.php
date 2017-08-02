<?php
require_once('TwitterApiFunctions.php');

class Test
{
	/**
    * A test function to process a complete task and return the final tweets.  
    *
    * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
    *
    * @return array :: array of tweets.
    */
    public function testing()
    {

        $getfield   = array(
            'q'     => '#custserv',
            'count' => '100'
            );

        $TwitterApiFuncInstance = new TwitterApiFunctions();

        $tweets     = $TwitterApiFuncInstance->searchTweets($getfield);

        if(sizeof($tweets) == 0)
        {
            print_r("No tweets to display");
            return array();
        }

        $tweet_keys = array(
            "retweet_count" => array(
                    "greater" => 0,
                    )
            );
        $tweets     = $TwitterApiFuncInstance->getRefineTweets($tweets,$tweet_keys);

        return $tweets;

    }
}

?>
<!--
A simple html page showing the resultant tweets in table format.

@warning It may happen that the page keeps on waiting, in that case, stop and reload the page.

@author Chinmay Rakshit <chinmay.rakshit@gmail.com> 

-->
<!DOCTYPE html>
<html>
<head>
    <title>Twitter Api Client</title>
    <style type="text/css">
    table, th, td {
        border-spacing: 0;
        border: 1px solid black;
    }
    th {
        height: 30px;
        background: grey;
    }
    </style>
</head>
<body>
<center>
    <h1>TWITTER TWEET ANALYSIS</h1><br>
    <table>
        <tr>
            <th>Tweet ID</th>
            <th>Retweet Count</th>
            <th>Tweet</th>
        </tr>
    <?php
        $start_time  = time();
        $tweets = testing();
        foreach ($tweets as $value) 
        {
            ?><tr>
            <td><?php echo $value['id_str'];?></td>
            <td align="center"><?php echo $value['retweet_count'];?></td>
            <td><?php echo str_ireplace('#custserv','<b>#custserv</b>',utf8_decode($value['text']));?></td>
            </tr><?php
        }
    ?>
</table>
</center>
</body>
</html>
<?php
$end_time = time();
print_r("total time: " . (string)($end_time-$start_time)."sec<br>");
print_r("total number of tweet: " . (string)(sizeof($tweets)));
?>