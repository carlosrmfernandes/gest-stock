import React, { useEffect } from "react";
import "./css/Products.css";
import verify from "../../hooks/autenticate";
function Products() {
  useEffect(() => {
    verify();
  });

  return (
    <div>
      <h1>Hello World</h1>
    </div>
  );
}

export default Products;
