import React from 'react';
import ReactDOM from 'react-dom';
import AlbumStar from './AlbumStar';

let star = $("#album-star-control");
let starNode = star.get(0);

if (starNode) {
  let isStarred = star.attr("data-starred") == "true";
  ReactDOM.render(
    <AlbumStar starred={isStarred} />,
    starNode
  );
}