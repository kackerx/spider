const {
    decrypt,
    decryptName
} = require('./play2')

const parser = require("@babel/parser");
// const template = require("@babel/template").default;
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;
const path = require('path');
const fs = require('fs')

const jscode = fs.readFileSync('/Users/k/Library/Mobile\ Documents/iCloud~com~coderforart~iOS~MWeb/Documents/mweb_documents_library/vim/learn-python/learn-python-spider/spider/sigu/source2.js', 'utf-8', () => {})

console.log(jscode)
var ast = parser.parse(jscode)

const visitor = {
    "CallExpression"(path) {
        var node = path.node
        if (node.callee.name === decryptName && node.arguments.length === 2) {
            console.log('======')
            var strC = decrypt(node.arguments[0].value, node.arguments[1].value)
            console.log(strC)
            path.replaceWith(t.stringLiteral(strC))
        }
    }
}

traverse(ast, visitor)

let {
    code
} = generator(ast)

fs.writeFileSync('/Users/k/Library/Mobile\ Documents/iCloud~com~coderforart~iOS~MWeb/Documents/mweb_documents_library/vim/learn-python/learn-python-spider/spider/sigu/decode2.js', code, 'utf-8', () => {})