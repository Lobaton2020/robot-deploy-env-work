
//config endpoints
const ENDPONTS = {
    init_eureka: "/deploy_server_eureka",
    init_selenium: "/insert_properties_zuul"
}



const manageMessage = {
    elemContainer: document.querySelector("#show-message"),
    elemSuccess: document.querySelector("#message-success"),
    elemError: document.querySelector("#message-error"),
    showSuccess() {
        this.elemContainer.classList.remove("d-none")
        this.elemSuccess.classList.remove("d-none")
        this.elemError.classList.add("d-none")
    },
    showError() {
        this.elemContainer.classList.remove("d-none")
        this.elemSuccess.classList.add("d-none")
        this.elemError.classList.remove("d-none")
    },
    close() {
        this.elemContainer.classList.add("d-none")
        this.elemSuccess.classList.add("d-none")
        this.elemError.classList.add("d-none")

    }
}

const btnTransform = {
    btn: null,
    idInterval: null,
    counter: document.querySelector("#time-run"),
    setBtn(btn) {
        this.btn = btn
    },
    loading() {
        const urlLoader = "https://abergeldie.com.au/wp-content/uploads/2015/12/ajax-loader-large.gif"
        this.btn.setAttribute("disabled", "on")
        this.btn.innerHTML = `
            <img src="${urlLoader}" style="width:40px"/>
            <span>Cargando...</span>
        `
        var count = 0;
        this.idInterval = setInterval(() => {
            let countNum = count < 10 ? "0" + count : count
            this.counter.innerHTML = `
                <span class="float-right d-flex aling-middle" >
                    <h4>${countNum}</h4>&nbsp;
                    <h6 class="mt-1">Segundos</h6>
                </span>
            `
            count++
        }, 1000);
    },
    finalSuccess() {
        this.btn.removeAttribute("disabled")
        this.btn.textContent = "INICAR SERVIDOR"
        this.btn.classList.remove("btn-info")
        this.btn.classList.add("btn-success")
        clearInterval(this.idInterval)
    },
    finalError() {
        this.btn.removeAttribute("disabled")
        this.btn.textContent = "VOLVER A INICAR SERVIDOR"
        this.btn.classList.add("btn-info")
        this.btn.classList.remove("btn-success")
        clearInterval(this.idInterval)
    }
}

const init = () => {
    const btn = document.querySelector("#btn-send")
    btn.addEventListener("click", function (e) {
        btnTransform.setBtn(this)
        btnTransform.loading()
        fetch(ENDPONTS.init_eureka)
            .then(res => res.json())
            .then(result => {
                if (result.status == 200) {
                    fetch(ENDPONTS.init_selenium)
                        .then(res => res.json())
                        .then(result => {
                            if (result.status == 200) {
                                btnTransform.finalSuccess()
                                manageMessage.showSuccess()
                            } else {
                                btnTransform.finalError()
                                manageMessage.showError()
                            }
                        }).catch(err => {
                            console.log(err)
                            btnTransform.finalError()
                            manageMessage.showError()
                        })
                } else {
                    btnTransform.finalError()
                    manageMessage.showError()
                }
            }).catch(err => {
                console.log(err)
                btnTransform.finalError()
                manageMessage.showError()
            })
    });
};

document.addEventListener("DOMContentLoaded", init)
