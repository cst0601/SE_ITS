import React from 'react';
import ReactMarkdown from 'react-markdown';
function Image(props){
  return <img {...props} style={{maxWidth: '100%'}} />
}
export default class MarkDown extends React.Component {  // export default is the class that is accessable from outside
  render() {
    return (
      <ReactMarkdown
        source={this.props.source}
        renderers={{image: Image}}
      />

    )
  }

}
