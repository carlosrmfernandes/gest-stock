import React, { useEffect } from "react";
import verify from "../../hooks/autenticate";
function Items() {
  useEffect(() => {
    verify();
  });

  return (
    <div>
      <h1>Hello World</h1>
    </div>
  );
}

export default Items;
