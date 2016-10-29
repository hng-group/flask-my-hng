var $articleTitle = $('#article-title');
var $articleCategory = $('#article-category');
var $articleSummary = $('#article-summary');
var $articleContent = $('#article-content');
var $publishArticle = $('#publish-article');
var $draftArticle = $('#draft-article');
var $saveArticle = $('#save-article');
var $trashArticle = $('#trash-article');

function Article($articleTitle, $articleCategory, $articleSummary, $articleContent, articleStatus) {
    this.articleTitle = $articleTitle.val();
    this.articleCategory = $articleCategory.val();
    this.articleSummary = $articleSummary.val();
    this.articleContent = $articleContent.summernote('code');
    this.articleStatus = articleStatus;
}

Article.submitArticleForm = function(articleStatus, url) {
    articleObject = new Article($articleTitle, $articleCategory, $articleSummary, $articleContent, articleStatus);
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: url,
        data: JSON.stringify(articleObject),
        dataType: "json",
        success: function (data) {
            console.log(data);
            if (data.articleStatus === 'Published') {
                swal({
                    title: "Success",
                    text: "Article published",
                    type: "success",
                    confirmButtonColor: "#18a689"
                });
            } else if (data.articleStatus === 'Draft') {
                swal({
                    title: "Success",
                    text: "Article saved to draft",
                    type: "success",
                    confirmButtonColor: "#18a689"
                });
            }
            $($publishArticle).prop('disabled', true);
            $($draftArticle).prop('disabled', true);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            swal("Error", errorThrown, "error")
        }
    });
};

// Article.saveChangeArticleForm = function(mode) {
//     articleObject = new Article($articleTitle, $articleCategory, $articleSummary, $articleContent, mode);
//     $.ajax({
//         type: "POST",
//         contentType: "application/json; charset=utf-8",
//         url: '/front-page/cms/{{article.id}}/edit/',
//         data: JSON.stringify(articleObject),
//         dataType: "json",
//         success: function (data) {
//             if (data.mode === 'publish') {
//                 swal({
//                     title: "Success",
//                     text: "Article published",
//                     type: "success",
//                     confirmButtonColor: "#18a689"
//                 });
//             } else if (data.mode === 'draft') {
//                 swal({
//                     title: "Success",
//                     text: "Article saved to draft",
//                     type: "success",
//                     confirmButtonColor: "#18a689"
//                 });
//             }
//             $(publishArticle).prop('disabled', true);
//             $(draftArticle).prop('disabled', true);
//         },
//         error: function(XMLHttpRequest, textStatus, errorThrown) {
//             swal("Error", errorThrown, "error")
//         }
//     });
// };