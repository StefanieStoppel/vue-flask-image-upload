const path = require('path')

module.exports = {
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