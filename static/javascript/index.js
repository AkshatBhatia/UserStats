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
        created_at: "created_at",
        text: "This is a tweet text",
        favorite_count: "favorite_count",
        retweet_count: "retweet_count",
    },
    parse: function(data) {
        var date = new Date(data.created_at);
        var day = date.getDate();
        var monthIndex = date.getMonth();
        var year = date.getFullYear();
        data.created_date = monthIndex + '-' + day + '-' + year;
        return data;
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

app.Summary = Backbone.Model.extend({
    defaults: {
        original_tweet_count: "original_tweet_count",
        retweet_count: "retweet_count",
        replies_count: "replies_count",
        tweets_with_hashtags: "tweets_with_hashtags",
        tweets_with_mentions: "tweets_with_mentions"
    },
    url: '/twitterstats/summary'
});

app.summary = new app.Summary();

app.User = Backbone.Model.extend({
    defaults: {
        id_str: "id_str",
        name: "name",
        screen_name: "screen_name",
        location: 'location',
        created_at: 'created_at',
        profile_image_url: 'profile_image_url',
        follower_count: 'follower_count',
        favorite_count: 'favorite_count',
        statuses_count: 'statuses_count'
    },
    url: '/twitterstats/user'
});

app.user = new app.User();

app.UserView = Backbone.View.extend({
    tagName: 'h1',
    template: _.template($('#header-template').html()),
    render: function() {
        this.$el.html(this.template(app.user.toJSON()));
        return this;
    }
})

app.UserOverview = Backbone.View.extend({
    template: _.template($('#user-overview-template').html()),
    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
})

// Views
app.TweetView = Backbone.View.extend({
    tagName: 'tr',
    template: _.template($('#tweet-template').html()),
    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        return this; // enable chained calls
    }
});

var ENTER_KEY = 13;
app.AppView = Backbone.View.extend({
      el: $('.input-group'),
      userId: '#user',
      filtersId: '#filters option:selected',
      user: '',
      events: {
          'click #search-user': 'searchUser',
          'keydown' : 'keyPressEventHandler'
      },
      initialize: function () {
          app.tweets.on('reset', this.addAll, this);
          this.fetchUser();
          this.fetchTweets();
      },
      fetchUser: function() {
          app.user.fetch({
              data: {
                user: this.user
              },
              success: function(){
                  var view = new app.UserView();
                  this.$('#header').html(view.render().el);
              }
          });
      },
      fetchTweets: function () {
          var that = this;
          app.tweets.fetch({
              data: {
                  user: this.user,
                  filters: this.filters
              },
              success: function () {
                  that.drawGraph();
                  that.addAll();
              }
          });
          app.summary.fetch({
              data: {
                  user: this.user,
                  filters: this.filters
              },
              success: function () {
                  var userOverview = new app.UserOverview({model: app.summary});
                  this.$('#user-overview').empty();
                  this.$('#user-overview').append(userOverview.render().el);
                  that.drawPieChart();
              }
          });
      },
      addOne: function (tweet) {
          var view = new app.TweetView({model: tweet});
          $('#tweet-list').append(view.render().el);
      },
      addAll: function () {
          $('#tweet-list').empty();
          app.tweets.each(this.addOne, this);
      },
      keyPressEventHandler: function(e) {
          console.log("here " + e.which);
          if(e.which === ENTER_KEY) {
            this.searchUser();
          }
      },
      searchUser: function () {
          this.user = $(this.userId).val();
          var filterArray = _.map($(this.filtersId), function (d) {
              return {
                  name: $(d).parent().attr('label'),
                  value: d.text
              };
          });

          var x = _.groupBy(filterArray, function (d) {
              return d.name;
          })

          this.filters = _.map(_.allKeys(x), function (d) {
              var vall = _.map(x[d], function (d) {
                  return d['value']
              });
              return d.toString() + '=' + vall;
          }).join(";");

          this.fetchUser();
          this.fetchTweets();
      },
      drawGraph: function () {
          console.log("inside drawgraph");
          var retweet_data = app.tweets.toJSON().map(function (d) {
              return [d.created_at, d.retweet_count];
          }).sort();
          var favourite_data = app.tweets.toJSON().map(function (d) {
              return [d.created_at, d.favorite_count];
          }).sort();

          // create the chart
          return $('#chart1').highcharts('StockChart', {
              chart: {
                  alignTicks: false
              },
              title: {
                  text: "Likes and Retweets timeseries"
              },
              colors: ['#7cb5ec', '#90ed7d', '#8085e9', '#f7a35c',
                  '#f15c80', '#e4d354', '#8085e8', '#8d4653', '#91e8e1'],
              rangeSelector: {
                  selected: 5
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
              }, {
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
      },
      drawPieChart: function(){
          var summaryJson = app.summary.toJSON();
          var colorsArray = ['#7cb5ec', '#90ed7d', '#f7a35c', '#8085e9',
              '#f15c80', '#e4d354', '#8085e8', '#8d4653', '#91e8e1'];
          $('#pie_chart').highcharts({
              chart: {
                  plotBackgroundColor: null,
                  plotBorderWidth: null,
                  plotShadow: false,
                  type: 'pie'
              },
              colors: Highcharts.map(colorsArray, function (color) {
                  return {
                      radialGradient: {
                          cx: 0.5,
                          cy: 0.3,
                          r: 0.7
                      },
                      stops: [
                          [0, color],
                          [1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
                      ]
                  };
              }),
              title: {
                  text: 'Summary'
              },
              tooltip: {
                  pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
              },
              plotOptions: {
                  pie: {
                      allowPointSelect: true,
                      cursor: 'pointer',
                      dataLabels: {
                          enabled: true,
                          format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                          style: {
                              color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                          },
                          connectorColor: 'silver'
                      }
                  }
              },
              series: [{
                  name: 'Tweet Summary',
                  data: [
                      {
                          name: 'Original Tweets',
                          y: summaryJson.original_tweet_count,
                          sliced: true,
                          selected: true
                      },
                      {
                          name: 'Retweets',
                          y: summaryJson.retweet_count
                      },
                      {
                          name: 'Replies',
                          y: summaryJson.replies_count
                      }
                  ]
              }]
          });
      }
  }
);

var appView = new app.AppView();