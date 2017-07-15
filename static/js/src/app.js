import React from 'react';
import ReactDOM from 'react-dom';

let csrf = require('./csrf');

class AlbumStar extends React.Component {
  constructor(props) {
    super(props);
    let parts = window.location.pathname.split('/');
    let album_id = parts[parts.length - 1];
    let iconClasses = props.starred ? "fa fa-star" : "fa fa-star-o";
    this.state = {
      url: "/albums/star/"+album_id,
      starred: props.starred,
      iconClasses: iconClasses,
    };
  }

  toggleStar() {
    let headers = csrf.addHeader();
    fetch(this.state.url, {
      method: 'POST',
      headers: headers,
      credentials: "include"
    })
      .then(response => response.json())
      .then(() => {
        this.setStarred(!this.state.starred);
      });
  }

  setStarred(starred) {
    let iconClasses;
    if (starred)
      iconClasses = "fa fa-star";
    else
      iconClasses = "fa fa-star-o";
    this.setState({starred: starred, iconClasses: iconClasses});
  }

  render() {
    return (
      <a href="#" className="star-album" onClick={() => this.toggleStar()}>
        <i className={this.state.iconClasses} aria-hidden="true"></i>
      </a>
    )
  }
}

let star = $("#album-star-control");
let starNode = star.get(0);

if (starNode) {
  let isStarred = star.attr("data-starred") == "true";
  ReactDOM.render(
  <AlbumStar starred={isStarred} />,
  starNode
);
}