$(document).ready(() => {

    $("#text-form").submit((e) => {
        e.preventDefault();

        $("#response").css("display", "none");
        $(".loader").css("display", "block")

        var text = $("#text")[0].value;
        var formData = new FormData();
        formData.append("text", text)

        fetch("/submit", {
                method: "post",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                $("#symptom").text(data.class);
                $("#confidence").text(Math.round(data.confidence * 100) / 100 + "%");

                $(".loader").css("display", "none")
                $("#response").css("display", "block");
            });
    });
});