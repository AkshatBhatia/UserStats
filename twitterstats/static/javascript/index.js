/**
 * Created by akbhatia on 12/30/15.
 */
// your JS code goes here
var app = {}; // create namespace for our app

//Models
app.Tweet = Backbone.Model.extend({
    defaults: {
        id_str: "id_str",
        author: "Author",
        text: "This is a tweet text",
        favorite_count: "favorite_count",
        retweet_count: "retweet_count",
    }
});

// Collections
app.Tweets = Backbone.Collection.extend({
    model: app.Tweet,
    url: '/twitterstats/tweets',
    parse: function(data) {
        return data.tweets;
    }
});

app.tweets = new app.Tweets();

// Views
app.TweetView = Backbone.View.extend({
    tagName: 'tr',
    template: _.template($('#tweet-template').html()),
    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        return this; // enable chained calls
    }
});

app.AppView = Backbone.View.extend({
    el: '#twitterstatsapp',
    userId: '#user',
    filtersId: '#filters option:selected',
    user: '',
    headers: _.template('<tr><th>TweetId</th><th>Author</th><th>Text</th><th data-defaultsort="desc">Favorites</th><th>Retweets</th></tr>'),

    events: {
        "click .search": "searchUser",
    },
    initialize: function () {
        app.tweets.on('reset', this.addAll, this);
        this.fetchTweets();
    },
    fetchTweets: function() {
        var that = this;
        app.tweets.fetch({data: {user: this.user,
            filters: this.filters},
            success: function () {
                drawGraph();
                that.addAll();
            }});
    },
    addOne: function(tweet){
        var view = new app.TweetView({model: tweet});
        this.$('#tweet-list').append(view.render().el);
    },
    addAll: function(){
        console.log("Reset is called");
        this.$('#tweet-list').empty();
        app.tweets.each(this.addOne, this);
    },
    searchUser: function(){
        this.user = $(this.userId).val();
        var filterArray = _.map($(this.filtersId), function (d) {
            return { name: $(d).parent().attr('label'),
                value : d.text};
        });

        var x = _.groupBy(filterArray, function(d) {
            return d.name;
        })

        console.log(x);

        this.filters = _.map(_.allKeys(x), function(d) {
            var vall = _.map(x[d], function(d) {return d['value']});
            return d.toString() + '=' + vall; }).join(";");

        console.log(this.filters);

        this.fetchTweets();
    }
});

var appView = new app.AppView();

function drawGraph() {
    var retweet_data = app.tweets.toJSON().map(function(d){ return [d.created_at, d.retweet_count]; }).sort();
    var favourite_data = app.tweets.toJSON().map(function(d){ return [d.created_at, d.favorite_count]; }).sort();

    // create the chart
    return $('#chart1').highcharts('StockChart', {
        chart: {
            alignTicks: false
        },
        colors: ['#7cb5ec', '#90ed7d', '#f7a35c', '#8085e9',
            '#f15c80', '#e4d354', '#8085e8', '#8d4653', '#91e8e1'],
        rangeSelector: {
            selected: 5
        },

        title: {
            text: 'Retweet chart'
        },

        series: [{
            type: 'line',
            name: 'Retweet count',
            data: retweet_data,
            dataGrouping: {
                units: [[
                    'week', // unit name
                    [1] // allowed multiples
                ], [
                    'month',
                    [1, 2, 3, 4, 6]
                ]]
            }
        },{
            type: 'line',
            name: 'Favourite count',
            data: favourite_data,
            dataGrouping: {
                units: [[
                    'week', // unit name
                    [1] // allowed multiples
                ], [
                    'month',
                    [1, 2, 3, 4, 6]
                ]]
            }
        }]
    });
}

function retweet_ts() {
    return app.tweets.toJSON()
        .map(function(d) {
            return {x: d.created_at, y: d.retweet_count};
        }).reverse();
}

function favorite_ts() {
    return app.tweets.toJSON()
        .map(function(d) {
            return {x: d.created_at, y: d.favorite_count};
        }).reverse();
}

function tweetData() {
    return [
        {
            key: 'Retweet Count',
            values: retweet_ts()
        },
        {
            key: 'Favorite Count',
            values: favorite_ts()
        }
    ];
}

function xDomain() {
    return retweet_ts().map(function(d) { return d.x; });
}