import React from 'react';
import {addHeader} from './csrf';

class AlbumPrint extends React.Component {
  constructor(props) {
    super(props);
    let parts = window.location.pathname.split('/');
    let albumId = props.albumId;
    let iconClasses = props.saved ? "fa fa-print print-saved" : "fa fa-print";
    this.state = {
      url: "/albums/toggle/print/"+albumId,
      saved: props.saved,
      iconClasses: iconClasses,
    };
  }

  toggleSaved() {
    let headers = addHeader();
    fetch(this.state.url, {
      method: 'POST',
      headers: headers,
      credentials: "include"
    })
      .then(response => response.json())
      .then(() => {
        this.setSaved(!this.state.saved);
      });
  }

  setSaved(saved) {
    let iconClasses;
    if (saved)
      iconClasses = "fa fa-print print-saved";
    else
      iconClasses = "fa fa-print";
    this.setState({saved: saved, iconClasses: iconClasses});
  }

  render() {
    return (
      <a className="print-album" onClick={() => this.toggleSaved()}>
        <i className={this.state.iconClasses} aria-hidden="true"></i>
      </a>
    )
  }
}

module.exports = AlbumPrint;