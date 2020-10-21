const path = require("path");
const { VueLoaderPlugin } = require("vue-loader");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  entry: {
    main: "./frontend/main.js",
    dashboard: "./frontend/dashboard.js",
  },
  output: {
    filename: "js/[name].js",
    path: path.resolve(__dirname, "./brynweb/static"),
    publicPath: "/static/", // Match Django STATIC_URL
    chunkFilename: "[id]-[chunkhash].js",
    // explanation see https://pascalw.me/blog/2020/04/19/webpack-django.html
  },
  devServer: {
    writeToDisk: true, // Write files to disk in dev mode, so Django can serve the assets
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: "vue-loader",
      },
      {
        test: /\.js$/,
        loader: "babel-loader",
      },
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, "css-loader"],
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
          },
          {
            loader: "sass-loader",
          },
        ],
      },
    ],
  },
  resolve: {
    alias: {
      vue: "vue/dist/vue.esm-bundler.js",
      Mixins: path.resolve(__dirname, "./frontend/mixins/"),
      Components: path.resolve(__dirname, "./frontend/components/"),
    },
  },
  plugins: [
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({
      filename: "css/[name].css",
    }),
  ],
};
