import './Footer.css';

function Footer() {

var time = new Date();
var year = time.getFullYear();


  return (
    <div className="Footer-Div">
      <footer className="">
        
        
        <p className="handjet-font">@ItzDeme {year}</p>
        
      </footer>
    </div>
  );
}

export default Footer;