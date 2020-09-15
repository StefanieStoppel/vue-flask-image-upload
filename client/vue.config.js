const path = require('path')

module.exports = {
    publicPath: '/static',
    outputDir: '../server/static',
    css: {
        loaderOptions: {
            sass: {
                sassOptions: {
                    includePaths: [path.resolve(__dirname, './node_modules/compass-mixins/lib')],
                },
                prependData: `@import "@/assets/styles.scss";`
            }
        }
    }
};