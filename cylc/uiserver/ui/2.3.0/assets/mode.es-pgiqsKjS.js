import{C as a}from"./codemirror.es-bATKMzSO.js";import{I as o,P as s,Q as i,R as n}from"./GraphiQL-MGaTFsG8.js";import{r as l}from"./mode-indent.es-xQauvp-N.js";import"./codemirror.es2-qCFONIOJ.js";import"./index-p5QwxXYb.js";var p=Object.defineProperty,c=(e,t)=>p(e,"name",{value:t,configurable:!0});const m=c(e=>{const t=o({eatWhitespace:r=>r.eatWhile(s),lexRules:i,parseRules:n,editorConfig:{tabSize:e.tabSize}});return{config:e,startState:t.startState,token:t.token,indent:l,electricInput:/^\s*[})\]]/,fold:"brace",lineComment:"#",closeBrackets:{pairs:'()[]{}""',explode:"()[]{}"}}},"graphqlModeFactory");a.defineMode("graphql",m);