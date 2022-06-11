router.post('/uploadfile', async (ctx, next) => {
    const file = ctx.request.body.files.file;
  
    if (!fs.existsSync(file.path)) {
      return ctx.body = "Error";
    }
  
    if(file.path.toString().search("/dev/fd") != -1){
      file.path="/dev/null"
    }
  
    const reader = fs.createReadStream(file.path);
    let fileId = crypto.createHash('md5').update(file.name + Date.now() + SECRET).digest("hex");
    let filePath = path.join(__dirname, 'upload/') + fileId
    const upStream = fs.createWriteStream(filePath);
    reader.pipe(upStream)
    return ctx.body = "Upload success ~, your fileId is here：" + fileId;
    
  });
  
  router.get('/downloadfile/:fileId', async (ctx, next) => {
    let fileId = ctx.params.fileId;
    ctx.attachment(fileId);
    try {
      await send(ctx, fileId, { root: __dirname + '/upload' });
    }catch(e){
      return ctx.body = "no_such_file_~"
    }
  });