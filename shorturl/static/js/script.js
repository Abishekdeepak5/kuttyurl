const uls = document.querySelectorAll(".bottomnav");

uls.forEach((ul) => {
  console.log("Hello");
  const resetClass = ul.parentNode.getAttribute("class");
  const lis = ul.querySelectorAll("li");

  lis.forEach((li) => {
    li.addEventListener("click", (e) => {
      // e.preventDefault();
      // e.stopPropagation();
      const target = e.currentTarget;

      if (
        target.classList.contains("active") ||
        target.classList.contains("follow")
      ) {
        return;
      }

      ul.parentNode.setAttribute(
        "class",
        `${resetClass} ${target.getAttribute("data-where")}-style`
      );
console.log(resetClass);
console.log(ul.parentNode);
      lis.forEach((item) => clearClass(item, "active"));

      setClass(target, "active");
    });
  });
});

function clearClass(node, className) {
  node.classList.remove(className);
}

function setClass(node, className) {
  node.classList.add(className);
}