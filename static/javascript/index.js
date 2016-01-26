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

// D3 pair of timeseries for retweets and favorites
function drawGraph() {
    return nv.addGraph(function () {
        var chart = nv.models.multiBarChart()
                .height(500)
                .reduceXTicks(true)   //If 'false', every single x-axis tick label will be rendered.
                .rotateLabels(0)      //Angle to rotate x-axis labels.
                .showControls(false)   //Allow user to switch between 'Grouped' and 'Stacked' mode.
                .stacked(true)
                .x(function (d) {
                    return new Date(d.x);
                })
            ;

        chart.xAxis
            .tickFormat(function(d) { return d3.time.format("%Y-%m-%d")(d) });

        chart.yAxis
            .tickFormat(d3.format(',.f'));

        chart.xScale = d3.time.scale();

        d3.select('#chart1 svg')
            .attr("height", 500)
            .datum(tweetData())
            .transition().duration(100)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
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