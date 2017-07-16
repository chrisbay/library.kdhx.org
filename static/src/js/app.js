import React from 'react';
import ReactDOM from 'react-dom';
import AlbumStar from './AlbumStar';

$(".album-star-control").each(function(){
  let isStarred = $(this).attr("data-starred") == "true";
  let albumId = $(this).attr("data-album-id");
  ReactDOM.render(
    <AlbumStar starred={isStarred} albumId={albumId} />,
    $(this).get(0)
  );
});