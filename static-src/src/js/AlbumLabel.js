import React from 'react';
import {addHeader} from './csrf';

class AlbumLabelSheet extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      albums: []
    };
  }

  componentDidMount() {
    let headers = addHeader();
    fetch('/albums/labels-to-print/', {
      headers: headers,
      credentials: "include"
    })
    .then(response => response.json())
    .then((json) => {
      const albums = json.map(a => ({
        'id': a['pk'],
        'artist': a['fields']['artist'][0],
        'title': a['fields']['title'],
        'label': a['fields']['labels'].join(' / '),
        'created': a['fields']['created'],
        'fileUnder': a['fields']['artist'][1],
        'colorLeft': a['fields']['genre'][1],
        'colorRight': a['fields']['genre'][2],
        'hidden': false
      }));
      this.setState({albums: albums});
    });
  }

  addBlank(beforeId) {
    const albums = [];
    this.state.albums.forEach((a) => {
      if (a.id == beforeId) {
        albums.push({'id': 'blank-'+a.id, 'hidden': false})
      }
      albums.push(a);
    });
    this.setState({albums: albums});
  }

  removeLabel(id) {
    let hideLabel = function() {
      const albums = this.state.albums.map((a) => {
        if (a.id == id) {
          a.hidden = true;
          return a;
        }
        return a;
      });
      this.setState({albums: albums});
    };
    if ((''+id).includes('blank')) {
      (hideLabel.bind(this))(id);
    } else {
      let headers = addHeader();
      fetch('/albums/toggle/print/'+id, {
        headers: headers,
        credentials: "include",
        method: 'POST'
      })
      .then(response => response.json())
      .then((json) => {
        // TODO - add error handling
        (hideLabel.bind(this))(id);
      });
    }
  }

  renderLabel(data) {
    if (data.hidden) return '';
    let dateCreated = new Date(data.created);
    let dateStr = dateCreated.getFullYear() + '-' + dateCreated.getMonth() + '-' + dateCreated.getDate();
    return (<AlbumLabel 
      id={data.id} 
      key={data.id}
      artist={data.artist} 
      title={data.title}
      label={data.label}
      created={dateStr}
      fileUnder={data.fileUnder}
      colorLeft={data.colorLeft}
      colorRight={data.colorRight}
      removeHandler={this.removeLabel.bind(this)}
      addHandler={this.addBlank.bind(this)} />);
  }

  render() {
    return <div className="row">{this.state.albums.map(this.renderLabel.bind(this))}</div>;
  }
}

class AlbumLabel extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      id: props.id,
      artist: props.artist,
      title: props.title,
      label: props.label,
      created: props.created,
      fileUnder: props.fileUnder,
      colorLeft: props.colorLeft,
      colorRight: props.colorRight
    };
  }

  remove() {
    this.props.removeHandler(this.state.id);
  }

  addBlank() {
    this.props.addHandler(this.state.id);
  }

  render() {
    if ((''+this.state.id).includes('blank')) {
      return (
        <div className="col-4 label" id={this.state.id}>
          <div className="label-text ui-widget-content">
            <div className="label-controls">
              <a className="no-print add-label-control" href="#" onClick={this.addBlank.bind(this)}>
                  <i className="fa fa-plus-circle" aria-hidden="true"></i>
              </a>
              <a className="no-print remove-label-control" href="#" onClick={this.remove.bind(this)}>
                  <i className='fa fa-times-circle' aria-hidden='true'></i>
              </a>
            </div>
          </div>
        </div>
      );
    }
    return (
      <div className="col-4 label" id={this.state.id}>
        <div className="label-text ui-widget-content">
            <div className="info-block">
                <div>{this.props.created}</div>
                <strong>{this.props.fileUnder}</strong>
            </div>
            <div className="color-block">
                <div style={{backgroundColor: '#'+this.props.colorLeft}}></div>
                <div style={{backgroundColor: '#'+this.props.colorRight}}></div>
            </div>
            <div className="label-row">
                <strong>{this.props.artist}</strong>
            </div>
            <div className="label-row">
                {this.props.title}
            </div>
            <div className="label-row">
                {this.props.label}
            </div>
            <div className="label-controls">
                <a className="no-print add-label-control" href="#" onClick={this.addBlank.bind(this)}>
                    <i className="fa fa-plus-circle" aria-hidden="true"></i>
                </a>
                <a className="no-print remove-label-control" href="#" onClick={this.remove.bind(this)}>
                    <i className='fa fa-times-circle' aria-hidden='true'></i>
                </a>
            </div>
        </div>
      </div>
    )
  }
}

module.exports.AlbumLabel = AlbumLabel;
module.exports.AlbumLabelSheet = AlbumLabelSheet;