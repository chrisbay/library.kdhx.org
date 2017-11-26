import React from 'react';
import ReactDOM from 'react-dom';
import AlbumStar from './AlbumStar';
import AlbumPrint from './AlbumPrint';

$(".album-star-control").each(function(){
  let isStarred = $(this).attr("data-starred") == "true";
  let albumId = $(this).attr("data-album-id");
  ReactDOM.render(
    <AlbumStar starred={isStarred} albumId={albumId} />,
    $(this).get(0)
  );
});

$(".album-print-control").each(function(){
  let isSaved = $(this).attr("data-saved") == "true";
  let albumId = $(this).attr("data-album-id");
  ReactDOM.render(
    <AlbumPrint saved={isSaved} albumId={albumId} />,
    $(this).get(0)
  );
});