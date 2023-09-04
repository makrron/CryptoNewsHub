import React from 'react';
import 'font-awesome/css/font-awesome.min.css';

class ReloadButton extends React.Component {
  // Función para recargar la página
  reloadPage = () => {
    window.location.reload();
  };

  render() {
    const buttonStyle = {
      position: 'fixed',
      bottom: '20px', // Ajusta la posición vertical según tus preferencias
      right: '20px', // Ajusta la posición horizontal según tus preferencias
      zIndex: '1000', // Asegura que el botón esté en la parte superior de otros elementos
    };

    return (
      <button
        style={buttonStyle}
        onClick={this.reloadPage}
      >
        <i className="fa fa-refresh mr-2"></i>
      </button>
    );
  }
}

export default ReloadButton;
