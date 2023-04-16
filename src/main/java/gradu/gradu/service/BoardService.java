package gradu.gradu.service;

import gradu.gradu.domain.Board;
import gradu.gradu.domain.BoardFile;
import gradu.gradu.dto.BoardDTO;
import gradu.gradu.dto.BoardFileDTO;
import gradu.gradu.repository.BoardFileRepository;
import gradu.gradu.repository.BoardRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class BoardService {

    private final BoardRepository boardRepository;
    private final BoardFileRepository boardFileRepository;

    @Transactional
    public void save(BoardFileDTO boardFileDTO, BoardDTO boardDTO) throws IOException {

        Board board = Board.builder()
                .missingName(boardDTO.getMissingName())
                .missingAge(boardDTO.getMissingAge())
                .missingGender(boardDTO.getMissingGender())
                .missingPlace(boardDTO.getMissingPlace())
                .missingDate(boardDTO.getMissingDate())
                .boardTime(LocalDateTime.now())
                .fileAttached(boardFileDTO.getBoardFile() == null || boardFileDTO.getBoardFile().isEmpty() ? 0 : 1)
                .build();
        Long saveId = boardRepository.save(board).getId();

        if (boardFileDTO.getBoardFile() != null && !boardFileDTO.getBoardFile().isEmpty()) {
            //첨부 파일있음
            MultipartFile boardFile = boardFileDTO.getBoardFile();
            String originalFilename = boardFile.getOriginalFilename();
            String storedFileName = System.currentTimeMillis() + "_" + originalFilename;
            String savePath = "C:/temp/" + storedFileName;
            boardFile.transferTo(new File(savePath));

            BoardFile toboardFile = BoardFile.builder()
                    .originalFileName(originalFilename)
                    .board(board)
                    .storedFileName(storedFileName)
                    .boardTime(board.getBoardTime())
                    .build();


            boardFileRepository.save(toboardFile);

            Path sourcePath = Paths.get(savePath);
            Path destinationPath = Paths.get("src/main/resources/static/board/" + storedFileName);
            try {
                Files.move(sourcePath, destinationPath);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

//
//        RestTemplate restTemplate = new RestTemplate();
//        HttpHeaders headers = new HttpHeaders();
//        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
//
//        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
//        if (savePath != null) {
//            body.add("boardFile", new FileSystemResource(new File(savePath)));
//        }
//        body.add("missingName", boardDTO.getMissingName());
//        body.add("missingAge", boardDTO.getMissingAge());
//        body.add("missingGender", boardDTO.getMissingGender());
//        body.add("missingPlace", boardDTO.getMissingPlace());
//        body.add("missingDate", boardDTO.getMissingDate());
//        body.add("boardTime", board.getBoardTime());
//        body.add("fileAttached", board.getFileAttached());
//
//        HttpEntity<MultiValueMap<String, Object>> request = new HttpEntity<>(body, headers);
//        String url = "http://localhost:4000/api/boards";
//
//        try {
//            ResponseEntity<Void> response = restTemplate.postForEntity(url, request, Void.class);
//            if (response.getStatusCode() == HttpStatus.OK) {
//                // 성공적으로 처리된 경우
//                System.out.println("성공!");
//            } else {
//                // 오류가 발생한 경우
//                System.out.println("실패!");
//            }
//        } catch (HttpClientErrorException e) {
//            // HTTP 요청 실패 시 예외 처리
//            System.out.println("HTTP 요청 실패: " + e.getMessage());
//        }
    }

    public List<BoardDTO> findAll() {
        List<Board> boards = boardRepository.findAll();
        List<BoardDTO> boardDTOS = new ArrayList<>();
        for (Board board : boards) {
            BoardDTO dto = BoardDTO.builder()
                    .id(board.getId())
                    .missingName(board.getMissingName())
                    .missingAge(board.getMissingAge())
                    .missingGender(board.getMissingGender())
                    .missingPlace(board.getMissingPlace())
                    .missingDate(board.getMissingDate())
                    .boardTime(board.getBoardTime())
                    .build();

            BoardFile boardFile = boardFileRepository.findByBoard(board);
                if (boardFile != null) {
                    BoardFileDTO boardFileDTO = BoardFileDTO.builder()
                            .originalFileName(boardFile.getOriginalFileName())
                            .storedFileName(boardFile.getStoredFileName())
                            .build();
                    dto.setBoardFileDTO(boardFileDTO);
                }

            boardDTOS.add(dto);
        }
        return boardDTOS;
    }


//    public Page<BoardDTO> paging(Pageable pageable) {
//        int page = pageable.getPageNumber() -1;//
//        int pageLimit= 3; // 한 페이지에 보여줄 글 개수
//        //한 페이지당 3개씩 글을 보여주고 정렬 기준은 id 기준으로 내림차순 정렬
//
//        Page<Board> board= boardRepository.findAll(PageRequest.of(page, pageLimit, Sort.by(Sort.Direction.DESC, "id")));
//        /*
//        board.getContent() // 요청 페이지에 해당하는 글
//        board.getTotalElements() // 전체 글개수
//        board.getNumber()//DB로 요청한 페이지 번호
//        board.getTotalPages() // 전체 페이지 갯수
//        board.getSize() //한 페이지에 보여지는 글 개수
//        board.hasPrevious();//이전 페이지 존재 여부
//        board.isFirst() // 첫 페이지 여부
//        board.isLast()//마지막 페이지 여부
//         */
//        Page<BoardDTO> boardDTOS = board.map(boards -> new BoardDTO(boards.getMissingName(),boards.getMissingAge(),boards.getMissingGender(), boards.getMissingPlace(), boards.getMissingDate()));
//        return boardDTOS;
//    }
}
