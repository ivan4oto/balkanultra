const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    mode: 'development',
    entry: {
        base: './src/base/index.js',
        home: './src/home/index.js',
        register: './src/register/index.js',
        results: './src/results/index.js',
        athletes: './src/athletes/index.js',
        about: './src/about/index.js'
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].bundle.js',
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "[name].css"
        }),
        new webpack.ProvidePlugin({
            Popper: ['popper.js', 'default']
        }),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
          })
    ],
    module: {
        rules: [
            // styles loader
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "sass-loader"
                ],
            },
            // fonts loader
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            name: "fonts/[name].[ext]"
                        }
                    },
                ],
            },
            // svg inline 'data:image' loader
            {
                test: /\.svg$/,
                loader: "svg-url-loader"
            },
            // image loader
            {
                test: /\.(png|jpe?g|gif)$/i,
                use: [
                  {
                    loader: 'file-loader',
                    options: {
                        esModule: false
                    }
                  },
                ],
            },
        ]
    }
};