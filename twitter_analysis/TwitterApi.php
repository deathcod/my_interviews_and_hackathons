<?php


/**
 * Twitter_api : A simple Twitter-api client in php.
 *
 * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
 * @link 
 * 
 * Class TwitterApi
 */
class TwitterApi
{
    /**
    * @var string
    */
    private $oauth_access_token;

    /**
    * @var string
    */
    private $oauth_access_token_secret;

    /**
     * @var string
     */
    private $consumer_key;

    /**
     * @var string
     */
    private $consumer_secret;

    /**
     * @var string
     */
    private $getfield;

    /**
     * @var array
     */
    private $oauth;

    /**
     * @var string
     */
    private $url;

    const URL = 'https://api.twitter.com/1.1/';

    /**
     * Create the API acces object. Requires an array of keys::
     * 1) oauth access token
     * 2) oauth access token secret
     * 3) consumer key
     * 4) consumer secret
     * These are all available by creating your own application on https://apps.twitter.com/
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *
     * @param array keys
     */
    public function __construct(array $keys)
    {

        $this->oauth_access_token        = $keys['oauth_access_token'];
        $this->oauth_access_token_secret = $keys['oauth_access_token_secret'];
        $this->consumer_key              = $keys['consumer_key'];
        $this->consumer_secret           = $keys['consumer_secret'];
    }

    /**
     * Set the GET query parameter as string, example: '?q=#custserv&count=20'
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *  
     * @param array QueryParameters
     * 
     * @return TwitterApi Instance of self for method chaining
     */
    public function setGetParameters(array $QueryParameters)
    {
        $this->getfield = http_build_query($QueryParameters);
        return $this;
    }

    /**
     * Set the extension for the url, example: 'search/tweets.json'
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *  
     * @param string extension
     * 
     * @return TwitterApi Instance of self for method chaining
     */
    public function setUrlwithExtension($extension)
    {
        $this->url = self::URL . $extension;
        return $this;
    }

    /**
     * Get getfield string (simple getter)
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     * 
     * @return string :: this->getfield
     */
    public function getGetParameters()
    {
        return $this->getfield;
    }

    /**
     * Get getUrlwithExtension string (simple getter)
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     * 
     * @return string :: this->url
     */
    public function getUrlwithExtension()
    {
        return $this->url;
    }

    /**
     * Build the Oauth object using params set in construct
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *
     * @see https://dev.twitter.com/docs/api/1.1
     *
     * @return TwitterApi Instance of self for method chaining
     */
    public function buildOauth()
    {
        $oauth_access_token        = $this->oauth_access_token;
        $oauth_access_token_secret = $this->oauth_access_token_secret;
        $consumer_key              = $this->consumer_key;
        $consumer_secret           = $this->consumer_secret;

        $oauth = array(
            'oauth_consumer_key'     => $consumer_key,
            'oauth_nonce'            => time(),
            'oauth_signature_method' => 'HMAC-SHA1',
            'oauth_token'            => $oauth_access_token,
            'oauth_timestamp'        => time(),
            'oauth_version'          => '1.0'
        );

        if(isset($this->getfield))
        {
            parse_str($this->getfield,$getfieldarray);
            $oauth +=$getfieldarray;
        }

        $base_info                = $this->buildBaseString('GET', $oauth);
        $composite_key            = rawurlencode($consumer_secret) . '&' . rawurlencode($oauth_access_token_secret);
        $oauth_signature          = base64_encode(hash_hmac('sha1', $base_info, $composite_key, true));
        $oauth['oauth_signature'] = $oauth_signature;
        $this->oauth = $oauth;
        return $this;
    }

    /** 
    * Perform the actual data retrieval from the API
    * 
    * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
    * 
    * @return string json of tweets
    */
    public function makeRequest()
    {
        $header  = array( $this->buildAuthorizationHeader($this->oauth), 'Expect:');
        $options = array( CURLOPT_HTTPHEADER     => $header,
                          CURLOPT_HEADER         => false,
                          CURLOPT_URL            => $this->getUrlwithExtension() . '?' . $this->getGetParameters(),
                          CURLOPT_RETURNTRANSFER => true,
                          CURLOPT_SSL_VERIFYPEER => false);
        
        $feed    = curl_init();
        curl_setopt_array($feed, $options);
        $tweets    = curl_exec($feed);
        curl_close($feed);
        return $tweets;
    }

    /**
     * Private method to generate the base string used by cURL
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *
     * @param string $method
     * @param array  $params
     *
     * @return string Built base string
     */
    function buildBaseString($method, $params)
    {
        $r = array();
        ksort($params);
        foreach($params as $key=>$value)
        {
            $r[] = "$key=" . rawurlencode($value);
        }
        return $method . "&" . rawurlencode($this->getUrlwithExtension()) . '&' . rawurlencode(implode('&', $r));
    }

    /**
     * Private method to generate authorization header used by cURL
     *
     * @author Chinmay Rakshit <chinmay.rakshit@gmail.com> 
     *
     * @param array $oauth Array of oauth data generated by buildOauth()
     *
     * @return string $return Header used by cURL for request
     */
    function buildAuthorizationHeader($oauth)
    {
        $r      = 'Authorization: OAuth ';
        $values = array();

        foreach($oauth as $key=>$value)
        {
            $values[] = "$key=\"" . rawurlencode($value) . "\"";
        }

        $r .= implode(', ', $values);
        return $r;
    }
}