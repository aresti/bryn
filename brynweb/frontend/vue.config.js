const pages = {
  index: {
    entry: "src/main.js",
    template: "public/base.html",
    filename: "../../templates/base.html", // Used as base Django base template for non-Vue views
    title: "CLIMB | Cloud Infrastructure for Microbial Informatics",
    chunks: ["chunk-vendors", "chunk-common", "index"],
  },
  dashboard: {
    entry: "src/dashboard.js",
    template: "public/dashboard.html",
    filename: "../../templates/home/dashboard.html", // Used as Django template for the Vue SPA
    title: "CLIMB | Dashboard",
    chunks: ["chunk-vendors", "chunk-common", "index", "dashboard"],
  },
};

module.exports = {
  publicPath: "/static/vue/",
  outputDir: "./build/static/vue/",

  pages: pages,

  chainWebpack: (config) => {
    config.module
      .rule("md")
      .test(/\.md$/)
      .use("raw-loader")
      .loader("raw-loader");
  },
};
