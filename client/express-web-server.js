// Why is this called a static web server? See https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_web_server#summary. This might seem obvious to some people, but it is important that everyone is using the same terminology and definitions to prevent confusion.

// Code borrowed from https://github.com/GreensterRox/docker-static-node.js-web-server/blob/master/node-static-server.js

// ------------------------------
// Uncomment for live deployment in Kubernetes.
const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");
// ------------------------------
// -----------------------------------------
// Uncomment to test local production build.
// import express from "express";
// import { createProxyMiddleware } from "http-proxy-middleware";
// -----------------------------------------

const app = express();

// The host is set to localhost by default for a live deployment.
let expressHost = "http://localhost";
// The Express server port number is set to 80 by default for a live deployment.
let expressPort = "80";

let fastApiHost = expressHost;
let fastApiPort = "8000";

app.use(express.static("build"));
app.use("/api", createProxyMiddleware({ target: `${fastApiHost}:${fastApiPort}`, changeOrigin: true }));

app.listen(expressPort, () => {
  console.log(`Express web server listening at ${expressHost}:${expressPort}`);
});
