import React from 'react';
import Markdown from './mark_down.js';
import {Tabs, Tab} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
import { Global } from '../global.js'
import autosize from 'autosize';
import './text_area_with_file.css';
export default class TextAreaWithFile extends React.Component {  // export default is the class that is accessable from outside
  constructor(props) {
    super(props)
    this.state = {
      hightlight: false
    }
    this.fileInputRef = React.createRef();
    this.handleChange = this.handleChange.bind(this);
    this.onDrop = this.onDrop.bind(this);
    this.onDragLeave = this.onDragLeave.bind(this);
    this.onDragOver = this.onDragOver.bind(this);
    this.openFileDialog = this.openFileDialog.bind(this);

  }

  openFileDialog() {
    if (this.props.disabled) return
    this.fileInputRef.current.click()
  }

  onDragOver(event) {
    event.preventDefault()
    this.setState({ hightlight: true })
  }

  onDragLeave() {
    this.setState({ hightlight: false })
  }

  onDrop(event) {
    event.preventDefault()
    let formData = new FormData();
    let uploadedFile = event.dataTransfer.files[0];
    formData.append('file', uploadedFile);
    const axios = require('axios');
    let comment = this.props.comment
    axios.post(
      Global.backend_host + "/file",
      formData,
      {headers:{'Content-Type': 'multipart/form-data'}}
    ).then(
      response => {
        switch(response.data.info) {
          case "redirect":
            window.location = window.location.origin + response.data.location;
            break;
          case "success":
            const isImage = require('is-image');
            let imagePath = Global.backend_host + response.data.payload;
            this.props.onTextChange(comment + (isImage(imagePath) ? "!" : "") +"[" + uploadedFile.name + "]("+ imagePath + ")")
            break;
          case "failure":
            alert(response.data.payload);
            break;
          default:
            alert("Web broken. Please refresh this page.");
        }
      }
    );
    this.setState({ hightlight: false })
  }

  handleChange(event) { // what the fuck is this function, I had enough with syntax sugar :(
    const { name, value } = event.target;
    this.setState({ [name]: value });
    if(this.props.onTextChange)
      this.props.onTextChange(value)
  }

  componentDidMount(){
     this.textarea.focus();
     autosize(this.textarea);
  }

  render() {
    return (
      <Tabs defaultActiveKey="write" id="issue-tabs">
          <Tab eventKey="write" title="Write">
            <textarea
              style={{minHeight: '156px',
                      maxHeight: '700px'}}
              placeholder="support mark down!&#13;&#10;attach file by draging and droping" name="comment"
              className={`form-control markdown ${this.state.hightlight ? 'Highlight' : ''}`}
              onDragOver={this.onDragOver}
              onDragLeave={this.onDragLeave}
              onDrop={this.onDrop}
              ref={c=>this.textarea=c}
              value={this.props.comment} onChange={this.handleChange}
            >
            </textarea>
          </Tab>
          <Tab eventKey="preview" title="Preview">
            <div style={{minHeight: "156px",border: "1px solid #ced4da", borderRadius: "0.25rem", padding: "0.375rem 0.75rem"}}>
              <Markdown
                source={this.props.comment}
              />
            </div>
          </Tab>
      </Tabs>
    )
  }

}
