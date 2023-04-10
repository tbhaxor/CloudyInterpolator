const plugins =  [
   require("tailwindcss"),
   require("autoprefixer"),
]

console.log(process.env.NODE_ENV)
if (process.env.NODE_ENV == "production") {
   plugins.push(require("postcss-minify"))
}

module.exports = {
   plugins,
}

