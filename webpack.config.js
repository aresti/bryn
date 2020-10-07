const path = require("path");
const { VueLoaderPlugin } = require("vue-loader");

module.exports = {
  entry: {
    dashboard: "./frontend/dashboard/index.js",
  },
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "./brynweb/static/js"),
    publicPath: "/static/", // Match Django STATIC_URL
    chunkFilename: "[id]-[chunkhash].js",
  },
  devServer: {
    writeToDisk: true, // Write files to disk in dev mode, so Django can serve the assets
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: { presets: ["@babel/preset-env"] },
      },
      {
        test: /\.vue$/,
        loader: "vue-loader",
      },
    ],
  },
  resolve: {
    alias: {
      vue: "vue/dist/vue.esm-bundler.js",
    },
  },
  plugins: [new VueLoaderPlugin()],
};

// explanation see https://pascalw.me/blog/2020/04/19/webpack-django.html
